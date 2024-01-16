#%% Importing crucial libabaries
import streamlit as st 
import os
import pandas as pd  # pip install pandas openpyxl
try:
  import plotly.express as px
except ImportError:
  os.system('python -m pip install plotly')
import streamlit as st  # pip install streamlit
import base64
from datetime import datetime
from PIL import Image
from io import BytesIO
import requests
import altair as alt
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
print(df.info())
print(df.head())
# %%
#COnverting data
print(df['Streams'] )
df['Streams'] = [float(str(i).replace(",","")) for i in df['Streams']]
print(df['Streams'] )
df['Streams+'] = [float(str(i).replace(",","")) for i in df['Streams+']]
df['7Day'] = [float(str(i).replace(",","")) for i in df['7Day']]
df['7Day+'] = [float(str(i).replace(",","")) for i in df['7Day+']]
print(df.head())
# %%
df['Date'] = pd.to_datetime(df['Date'])
# Convert min and max dates to datetime objects
min_date = pd.to_datetime(df['Date'].min()).to_pydatetime()
max_date = pd.to_datetime(df['Date'].max()).to_pydatetime()

# Sidebar with date range slider
date_range = st.sidebar.slider('Select Date Range', min_value=min_date, max_value=max_date, value=(min_date, max_date))

# Clear Filters Button
if st.sidebar.button('Clear Filters'):
    date_range = (min_date, max_date)
    
# %%
# Streamlit code
st.title("Artist Images Dashboard")

# Select an artist
sorted_artist = sorted(df['Artist'].unique())
selected_artist = st.selectbox("Select an artist:", sorted_artist)
# Apply date range filter
filtered_df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
# Filter DataFrame based on selected filters
filtered_df = filtered_df[(filtered_df['Date'] >= date_range[0]) & (filtered_df['Date'] <= date_range[1])]

# Display the selected artist's image
selected_artist_image_url = filtered_df[filtered_df['Artist'] == selected_artist]['Images'].iloc[0]
response = requests.get(selected_artist_image_url)
img = Image.open(BytesIO(response.content))

# Layout
col1, col2, col3 = st.columns([1.0, 2, 2.2])

# Left column (frame)
with col1:
    st.markdown("## Artist Image:")
    col1.image(img, caption="", use_column_width=True)

# Middle column (frame)
with col2:
    st.markdown("## Artist Details:")
    st.header(selected_artist)
    st.subheader(f"Popularity: {filtered_df[filtered_df['Artist'] == selected_artist]['Popularity'].iloc[0]}")
    st.subheader(f"Followers: {filtered_df[filtered_df['Artist'] == selected_artist]['Followers'].iloc[0]}")
    st.subheader(f"Genres: {filtered_df[filtered_df['Artist'] == selected_artist]['Genres'].iloc[0]}")
# Right column (frame)
with col3:
    st.markdown("## Artist statistics:")
    st.subheader(f"Total Streams: {filtered_df[filtered_df['Artist'] == selected_artist]['Streams'].sum()}")
    st.subheader(f"Streams gain within 24h: {filtered_df[filtered_df['Artist'] == selected_artist]['Streams+'].max()}")

# %%
# Second row with charts and selections
col4, col5 = st.columns([2, 1])

# Bar Chart
chart_data = filtered_df[filtered_df['Artist'] == selected_artist].copy()
selected_songs = col5.multiselect("Select songs:", df[df['Artist'] == selected_artist]['Title'].unique())

if selected_songs:
    chart_data = chart_data[chart_data['Title'].isin(selected_songs)]

# Convert Date to datetime
print(chart_data['Date'])

chart_data['Date'] = pd.to_datetime(chart_data['Date'])

# Group the data by song titles and sum the streams within each song title
grouped_chart_data = chart_data.groupby(['Date', 'Title'])['Streams'].sum().reset_index()

chart_songs2 = px.bar(grouped_chart_data, x='Date', y='Streams', color='Title', title='Stream by song title:')

# Update x-axis properties
chart_songs2.update_xaxes(
    tickformat='%Y-%m-%d',  # Display only date without days
    tickangle=-45,  # Rotate x-axis labels by 90 degrees
)

# Display the chart with the updated x-axis
col4.plotly_chart(chart_songs2)
# Song Table
col5.subheader("Songs:")

if selected_songs:
    grouped_df = filtered_df[(filtered_df['Artist'] == selected_artist) & (filtered_df['Title'].isin(selected_songs))].sort_values(by=['Title', 'Date'])
    col5.dataframe(grouped_df[['Title', 'Streams', 'Streams+', 'Date']])
else:
    grouped_df = filtered_df[filtered_df['Artist'] == selected_artist].sort_values(by=['Title', 'Date'])
    col5.dataframe(grouped_df[['Title', 'Streams', 'Streams+', 'Date']])
    
# %%
# Third row with bubble chart
col6, col7 = st.columns([2, 1])
st.markdown("""---""")
# Bubble Chart
bubble_data = filtered_df[filtered_df['Artist'] == selected_artist].copy()

# Group the data by song titles and sum the streams and popularity within each song title
grouped_bubble_data = bubble_data.groupby('Title').agg({
    'Streams': 'sum',
    'Streams+': 'max',
    'Popularity': 'mean'  # You can choose another aggregation method if needed
}).reset_index()

bubble_chart = alt.Chart(grouped_bubble_data).mark_circle().encode(
    x=alt.X('Streams+:Q', axis=alt.Axis(title='Streams+')),
    y=alt.Y('Streams:Q', axis=alt.Axis(title='Streams')),
    size=alt.Size('Popularity:Q', title='Popularity'),
    color='Title:N',
    tooltip=['Streams+:Q', 'Title:N', 'Streams:Q', 'Popularity:Q']
).properties(
    width=1000,  # Adjust the width as needed
    height=300
)

# Display the bubble chart
col6.altair_chart(bubble_chart, use_container_width=True)
# %%
st.markdown("""---""")
