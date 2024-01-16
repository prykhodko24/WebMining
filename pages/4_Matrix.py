#%% Importing crucial libabaries
import streamlit as st 
import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
import requests
import altair as alt
import kaleido
from pathlib import Path
# %% ---- Logo update ----
st.sidebar.success("Select a section above")

path = Path(__file__).parent
# Use file protocol to load the image
logo_path = path / "Spotify-logo.png"

file_path = path / "Country_total - Copy.xlsx"

st.markdown(f"<img src='data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}' alt='Logo' width='100' style='float:left;margin-right:10px;'> **Artist analysis**", unsafe_allow_html=True)
# %%
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
# %% coNVERTING DaTA
df['Streams'] = [float(str(i).replace(",","")) for i in df['Streams']]
df['Followers'] = [float(str(i).replace(",","")) for i in df['Followers']]
df['Popularity'] = [float(str(i).replace(",","")) for i in df['Popularity']]
df['Streams+'] = [float(str(i).replace(",","")) for i in df['Streams+']]
df['7Day'] = [float(str(i).replace(",","")) for i in df['7Day']]
df['7Day+'] = [float(str(i).replace(",","")) for i in df['7Day+']]
print(df.head())
df['Artist&Title'] = df['Artist'] + ' - ' + df['Title']

# %%
df['Date'] = pd.to_datetime(df['Date'])
# Convert min and max dates to datetime objects
min_date = pd.to_datetime(df['Date'].min()).to_pydatetime()
max_date = pd.to_datetime(df['Date'].max()).to_pydatetime()


#Please select 
st.sidebar.header("Please filter here:")

# Sidebar with date range slider
date_range = st.sidebar.slider('Select Date Range', min_value=min_date, max_value=max_date, value=(min_date, max_date))

selected_country = st.sidebar.selectbox("Select Country", df['Country'].unique())

# Streams filter slider

df=df.dropna(subset="Streams")    
streams_filter = st.sidebar.slider("Select Streams Range", min_value=df['Streams'].min(), max_value=df['Streams'].max(), value=(df['Streams'].min(), df['Streams'].max()))
# Followers filter
df=df.dropna(subset="Followers")    
followers_filter = st.sidebar.slider("Select Followers Range", min_value=df['Followers'].min(), max_value=df['Followers'].max(), value=(df['Followers'].min(), df['Followers'].max()))
# Filter for X and Y dimensions
dimensions = ['Streams', 'Streams+', '7Day', '7Day+', 'Followers', 'Popularity']
x_axis_dimensions = st.sidebar.multiselect("X-Axis Dimension", dimensions, default=[dimensions[0]])
y_axis_dimensions = st.sidebar.multiselect("Y-Axis Dimension", dimensions, default=[dimensions[1]])


# Check if the dimensions are the same
if set(x_axis_dimensions) & set(y_axis_dimensions):
    st.warning("Please select different dimensions for X-Axis and Y-Axis.")
else:
    # Color Dimension filter as multi-select
    color_dimensions = st.sidebar.multiselect("Color Dimension", ['Artist', 'Title', 'Genres', 'Artist&Title'], default=[])

    # Size Dimension filter as multi-select
    size_dimensions = st.sidebar.multiselect("Size Dimension", ['Streams', 'Streams+', 'Followers', 'Popularity', '7Day', '7Day+'], default=[])

    # Apply Filters
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Streams'] >= streams_filter[0]) & (df['Streams'] <= streams_filter[1]) &
    (df['Followers'] >= followers_filter[0]) & (df['Followers'] <= followers_filter[1]) &
    (df['Country'] == selected_country) &
    (df[x_axis_dimensions[0]] == df[x_axis_dimensions[0]]) & (df[y_axis_dimensions[0]] == df[y_axis_dimensions[0]])  # Additional conditions to ensure different dimensions
]

# Clear Filters Button
if st.sidebar.button('Clear Filters'):
    date_range = (min_date, max_date)

# Create Scatter Plot
fig = px.scatter(
    filtered_df,
    x=x_axis_dimensions[0],
    y=y_axis_dimensions[0],
    color=color_dimensions[0] if color_dimensions else None,
    size=size_dimensions[0] if size_dimensions else None,
    title="Matrix chart:",
    labels={x_axis_dimensions[0]: x_axis_dimensions[0], y_axis_dimensions[0]: y_axis_dimensions[0]}
)

# Show the chart
st.plotly_chart(fig, use_container_width=True, width=10000, height=20000, config={'displayModeBar': False})
# %%