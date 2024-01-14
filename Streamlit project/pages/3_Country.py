# %%
# Importing crucial libabaries
import streamlit as st 
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import base64
from datetime import datetime
import pydeck as pdk
import plotly.offline as pyo
from streamlit_echarts import st_echarts
import matplotlib.pyplot as plt
import squarify
import seaborn as sns
from pathlib import Path
#  ---- Logo update ----
st.sidebar.success("Select a section above")

path = Path(__file__).parent
# Use file protocol to load the image
logo_path = path / "Spotify-logo.png"

file_path = path / "Country_total - Copy.xlsx"

st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}' alt='Logo' width='100' style='float:left;margin-right:10px;'> **General**", unsafe_allow_html=True)
# %% loading excel data
def get_data_from_excel(file_path):
    df = pd.read_excel(
        io=file_path,
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:M",
        nrows=3831,
    )
    
    
    
    return df
df = get_data_from_excel(file_path)
# %%
#COnverting data

df['Streams'] = [float(str(i).replace(",","")) for i in df['Streams']]
df['Streams+'] = [float(str(i).replace(",","")) for i in df['Streams+']]
df['7Day'] = [float(str(i).replace(",","")) for i in df['7Day']]
df['7Day+'] = [float(str(i).replace(",","")) for i in df['7Day+']]

# %%
st.sidebar.header("Please Filter Here:")
continent = st.sidebar.selectbox(
    "Select the Continent:",
    options=df["Continent"].unique()
)

# Filter DataFrame based on selected continent
filtered_df = df[df['Continent'] == continent]

# Convert dates to datetime objects
df['Date'] = pd.to_datetime(df['Date'])
min_date = pd.to_datetime(df['Date'].min()).to_pydatetime()
max_date = pd.to_datetime(df['Date'].max()).to_pydatetime()

# Sidebar with date range slider
date_range = st.sidebar.slider('Select Date Range', min_value=min_date, max_value=max_date, value=(min_date, max_date))

# Filter DataFrame based on selected date range
filtered_df = filtered_df[(filtered_df['Date'] >= date_range[0]) & (filtered_df['Date'] <= date_range[1])]

# Group by country and sum the 'Streams'
grouped_df = filtered_df.groupby('Country')['Streams+'].sum().reset_index()

# Sort the values in descending order
sorted_df = grouped_df.sort_values(by='Streams+', ascending=False)


left_column, right_column = st.columns(2)
with left_column:

    # Bar chart for grouped and sorted data
        bar_chart = px.bar(
         sorted_df,
            x='Country',
            y='Streams+',
            title='Biggest Streams gainers/lossers in 24h',
        labels={'Streams+': 'Total Streams'},
        )
        st.plotly_chart(bar_chart)

        # Group by country and sum the 'Streams'
        grouped_df = filtered_df.groupby('Country')['7Day+'].sum().reset_index()

        # Sort the values in descending order
        sorted_df = grouped_df.sort_values(by='7Day+', ascending=False)
with right_column:
    # Bar chart for grouped and sorted data
        bar_chart2 = px.bar(
            sorted_df,
            x='Country',
            y='7Day+',
            title='Biggest Streams gainers/lossers in 7Day',
            labels={'7Day+': 'Total Streams'},
        )
        st.plotly_chart(bar_chart2)



bottom_left_column, bottom_right_column = st.columns(2)

with bottom_left_column:
    # Heat map with squarify
    heatmap_data = filtered_df.groupby('Country')['Streams'].sum().reset_index()

    heatmap_fig, ax = plt.subplots(figsize=(12, 8))
    squarify.plot(sizes=heatmap_data['Streams'], label=heatmap_data['Country'], alpha=0.7, color=sns.color_palette('viridis', n_colors=len(heatmap_data)))
    plt.axis('off')  # Turn off axis
    plt.title('Streams for Selected Continent')
    st.pyplot(heatmap_fig)
# %%
# map chart
with bottom_right_column:
    country_data = {
    'Country': [
        'Italy', 'United Kingdom', 'Australia', 'Sweden', 'Canada',
        'Argentina', 'Peru', 'Turkey', 'Philippines', 'Spain',
        'Colombia', 'United States', 'Germany', 'Czech Republic', 'Paraguay',
        'Honduras', 'New Zealand', 'Portugal', 'Costa Rica', 'Romania',
        'Switzerland', 'Hong Kong', 'Egypt', 'Venezuela', 'Kazakhstan',
        'Bolivia', 'Singapore', 'Nicaragua', 'Uruguay', 'United Arab Emirates',
        'Slovakia', 'Hungary', 'Thailand', 'Panama', 'Austria', 'Ukraine',
        'Israel', 'Dominican Republic', 'Chile', 'Netherlands', 'Norway',
        'Malaysia', 'Ecuador', 'El Salvador', 'Lithuania', 'Saudi Arabia',
        'Pakistan', 'France', 'Poland', 'Vietnam', 'Indonesia', 'South Korea',
        'Mexico', 'Japan', 'Guatemala', 'Belgium', 'Taiwan', 'Estonia',
        'Morocco', 'Latvia', 'Bulgaria', 'Global', 'Ireland', 'Brazil',
        'Denmark', 'India', 'South Africa', 'Finland', 'Luxembourg', 'Iceland',
        'Greece', 'Russia', 'Malta', 'Belarus', 'Nigeria'
    ],
    'ISO_Code': [
        'ITA', 'GBR', 'AUS', 'SWE', 'CAN', 'ARG', 'PER', 'TUR', 'PHL', 'ESP',
        'COL', 'USA', 'DEU', 'CZE', 'PRY', 'HND', 'NZL', 'PRT', 'CRI', 'ROU',
        'CHE', 'HKG', 'EGY', 'VEN', 'KAZ', 'BOL', 'SGP', 'NIC', 'URY', 'ARE',
        'SVK', 'HUN', 'THA', 'PAN', 'AUT', 'UKR', 'ISR', 'DOM', 'CHL', 'NLD',
        'NOR', 'MYS', 'ECU', 'SLV', 'LTU', 'SAU', 'PAK', 'FRA', 'POL', 'VNM',
        'IDN', 'KOR', 'MEX', 'JPN', 'GTM', 'BEL', 'TWN', 'EST', 'MAR', 'LVA',
        'BGR', 'XXX', 'IRL', 'BRA', 'DNK', 'IND', 'ZAF', 'FIN', 'LUX', 'ISL',
        'GRC', 'RUS', 'MLT', 'BLR', 'NGA'
    ]
}
    df_countries = pd.DataFrame(country_data)
    df = pd.merge(df, df_countries, on="Country", how='left')

    # Choropleth map of streams over time
    choropleth_map = px.choropleth(
        df,
        locations='ISO_Code',
        color='Streams',
        animation_frame='Date',
        title='Streams distribution Over Time',
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'Streams': 'Streams'},
        projection='natural earth'
    )
    st.plotly_chart(choropleth_map)