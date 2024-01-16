# %% Importing crucial libabaries
import os 
import streamlit as st 
try:
  import pandas as pd
except ImportError:
  os.system('python -m pip install pandas')

try:
  import plotly.express as px
except ImportError:
  os.system('python -m pip install plotly')
os.system('python -m pip install openpyxl')
import openpyxl
import base64
from datetime import datetime
from pathlib import Path
# %% ---- Logo update ----
st.sidebar.success("Select a section above")

path = Path(__file__).parent
# Use file protocol to load the image
logo_path = path / "Spotify-logo.png"

file_path = path / "Country_total - Copy.xlsx"

mostview_path = path / "Top_years.xlsx"

topartist_path = path / "Top_2500_total.xlsx"

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
print(df.info())
# %%
#COnverting data

df['Streams'] = [float(str(i).replace(",","")) for i in df['Streams']]
df['Streams+'] = [float(str(i).replace(",","")) for i in df['Streams+']]
df['7Day'] = [float(str(i).replace(",","")) for i in df['7Day']]
df['7Day+'] = [float(str(i).replace(",","")) for i in df['7Day+']]
print(df.head())
# %% loading excel data
def get_data_from_excel(mostview_path):
    df_mostviewed = pd.read_excel(
        io=mostview_path,
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:E",
        nrows=24,
    )
    
    
    
    return df_mostviewed
df_mostviewed = get_data_from_excel(mostview_path)
# %% loading excel data
def get_data_from_excel(topartist_path):
    df_artists = pd.read_excel(
        io=topartist_path,
        engine="openpyxl",
        sheet_name="Sheet1",
        usecols="A:G",
        nrows=31,
    )
    
    
    return df_artists
df_artists = get_data_from_excel(topartist_path)

df_artists['Streams'] = [float(str(i).replace(",","")) for i in df_artists['Streams']]
df_artists['Daily'] = [float(str(i).replace(",","")) for i in df_artists['Daily']]
# %%
print(df_artists.info())
# %%
st.sidebar.header("Please Filter Here:")
country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique(),
    default=[]
)

artist = st.sidebar.multiselect(
    "Select the Artist:",
    options=df["Artist"].unique(),
    default=[]
)

# %%
df['Date'] = pd.to_datetime(df['Date'])
# Convert min and max dates to datetime objects
min_date = pd.to_datetime(df['Date'].min()).to_pydatetime()
max_date = pd.to_datetime(df['Date'].max()).to_pydatetime()

# Sidebar with date range slider
date_range = st.sidebar.slider('Select Date Range', min_value=min_date, max_value=max_date, value=(min_date, max_date))

# Filter DataFrame based on selected filters
filtered_df = df
if country:
    filtered_df = filtered_df[filtered_df['Country'].isin(country)]
if artist:
    filtered_df = filtered_df[filtered_df['Artist'].isin(artist)]
filtered_df = filtered_df[(filtered_df['Date'] >= date_range[0]) & (filtered_df['Date'] <= date_range[1])]

# %% TOP KPI's - # Display total streams, artist with most streams, most streamed song, and count of countries
filtered_df['Streams']=[float(str(i).replace(',','')) for i in filtered_df['Streams']]
total_streams = filtered_df['Streams'].sum()
most_streamed_artist = filtered_df.groupby('Artist')['Streams'].sum().idxmax()
# filtered_df['Streams+']=[float(str(i).replace(',','').replace('+','')) for i in filtered_df['Streams+']]
filtered_df['Streams+']=[float(str(i).replace(',','')) for i in filtered_df['Streams+']]

biggest_streams_gainer = filtered_df.loc[filtered_df['Streams+'].idxmax(), 'Artist']



# Get most streamed songs from the "Top_years" table
df_most_streamed_songs = df_mostviewed[(df_mostviewed['Type'] == 'Most streamed songs') & (df_mostviewed['Each Year'] == 'Of all time')]

most_streamed_songs = ', '.join(df_most_streamed_songs['Artist and Title'])

# Get most streamed album from the "Top_years" table
df_most_streamed_album = df_mostviewed[(df_mostviewed['Type'] == 'Most streamed albums') & (df_mostviewed['Each Year'] == 'Of all time')]

most_streamed_album = ', '.join(df_most_streamed_album['Artist and Title'])

# Get the artist with the most followers from the filtered data
max_date_filtered = df['Date'].max()
top_followed_artist_filtered = df[df['Date'] == max_date_filtered].groupby('Artist')['Followers'].max().idxmax()

# Display second row of KPIs in three columns
left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Most Streamed Songs of All Time:")
    st.text(most_streamed_songs)

with middle_column:
    st.subheader("Most Streamed Album of All Time:")
    st.text(most_streamed_album)

with right_column:
    st.subheader("Artist with Most Followers in Selected Country:")
    st.text(top_followed_artist_filtered)



# Display second row of KPIs
st.markdown("""---""")




# column distribution 
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Streams:")
    st.text(f"{total_streams:,}")
with middle_column:
    st.subheader("Most streamed artist:")
    st.text(f"{most_streamed_artist}")
with right_column:
    st.subheader("Most streams gained artist:")
    st.text(f"{biggest_streams_gainer}")

st.markdown("""---""")

# %%
# Change the format of the "Date" column to YYYY-MM-DD
filtered_df['Date'] = filtered_df['Date'].dt.strftime('%Y-%m-%d')
# %%
# Display top streams DataFrame on the left column
left_column, right_column = st.columns([2,2]) 

with left_column:
    st.subheader("All Streams:")
    selected_columns = ['Date','Country', 'Artist', 'Title', 'Streams', 'Streams+']
    st.dataframe(filtered_df[selected_columns])
with right_column:   
    if artist and country:
    # If both artist and country are selected, display data for the specific artist in the specific country
        specific_artist_in_specific_country = filtered_df[(filtered_df['Country'] == country[0]) & (filtered_df['Artist'] == artist[0])]

        fig_specific_artist_in_specific_country = px.bar(specific_artist_in_specific_country,
                                                     x='Date',
                                                     y='Streams',
                                                     color='Title',
                                                     labels={'Streams': 'Total Streams'},
                                                     title=f'Streams Over Time for {artist[0]} in {country[0]}')     
        st.plotly_chart(fig_specific_artist_in_specific_country)

    elif artist:
        # If only an artist is selected, display top 10 countries where the artist was streamed
        top_countries_by_artist = filtered_df[filtered_df['Artist'] == artist[0]].groupby('Country')['Streams'].sum().nlargest(10).reset_index()
        top_countries_by_artist = top_countries_by_artist.sort_values(by='Streams', ascending=True)
        fig_top_countries_by_artist = px.bar(top_countries_by_artist,
                                         x='Streams',
                                         y='Country',
                                         labels={'Streams': 'Total Streams'},
                                         title=f'Top 10 Countries for {artist[0]}')

    elif country:
        # If only a country is selected, display top 10 streamed artists in that country
        top_artists_by_country = filtered_df[filtered_df['Country'].isin(country)].groupby('Artist')['Streams'].sum().nlargest(10).reset_index()
        top_artists_by_country = top_artists_by_country.sort_values(by='Streams', ascending=True)
        fig_top_artists_by_country = px.bar(top_artists_by_country,
                                        x='Streams',
                                        y='Artist',                                        
                                        labels={'Streams': 'Total Streams'},
                                        title=f'Top 10 Artists in {", ".join(country)}')
        st.plotly_chart(fig_top_artists_by_country)

    else:
         # If neither artist nor country is selected, display top streams for "Global" only
        top_streams_global = filtered_df.groupby('Title')['Streams'].sum().nlargest(10).reset_index()
        top_streams_global = top_streams_global.sort_values(by='Streams', ascending=True) 

        fig_top_streams_global = px.bar(top_streams_global,
                                    x='Streams',
                                    y='Title',
                                    labels={'Streams': 'Total Streams'},
                                    title='Top Streams Globally',
                                    orientation='h')
                                 
        st.plotly_chart(fig_top_streams_global)

st.markdown("""---""")
# %%
print("df_mostviewed",df_mostviewed.info())
df_songs = df_mostviewed[df_mostviewed['Type'] == 'Most streamed songs']
print(df_songs.info())
df_songs['Most streamed songs'] = (df_songs[['Each Year', 'Artist and Title']].astype(str) + ' ').sum(axis=1).str.strip()
print(df_songs.info())
# %%
# Display charts for most streamed songs, genres, and top 10 artists on the second row
bottom_left_column, bottom_right_column = st.columns(2)

with bottom_left_column:
    # Group the data by genre and sum the streams within each genre
    grouped_df = filtered_df.groupby(['Date', 'Genres'])['Streams'].sum().reset_index()
    
    # Create the stacked bar chart with the grouped data
    fig_stacked_bar = px.bar(grouped_df, 
                             x='Date', 
                             y='Streams', 
                             color='Genres', 
                             title='Streams by Genre Over Time',
                             labels={'Streams': 'Total Streams'},
                             height=400)
    
    st.plotly_chart(fig_stacked_bar)
# %%

with bottom_right_column:
#Create a pie chart for top 10 artists
    df_artists_sorted = df_artists.sort_values(by='Streams', ascending=False)
    top_10_artists = df_artists.head(10)

# Group the rest of the artists as "Others"
    other_artists = pd.DataFrame({
     'Artist': ['Others'],
        'Streams': [df_artists['Streams'][10:].sum()]
    })

    # Concatenate top 10 and "Others"
    pie_chart_data = pd.concat([top_10_artists, other_artists])

    # Create a pie chart
    fig_pie_chart = px.pie(pie_chart_data, values='Streams', names='Artist', title='Top 10 Artists and Others by Streams')
    # Display the pie chart
    st.plotly_chart(fig_pie_chart)

st.markdown("""---""")
# Get the maximum date in the filtered dataframe
max_date_filtered = filtered_df['Date'].max()

# Filter the dataframe to get the latest data for each artist in the selected country
df_max_date_filtered = filtered_df[filtered_df['Date'] == max_date_filtered]

# Select unique followers values for each artist in the selected country
top_followed_artists_filtered = df_max_date_filtered.groupby('Artist')['Followers'].max().nlargest(10).reset_index()

# Sort the dataframe in ascending order
top_followed_artists_filtered = top_followed_artists_filtered.sort_values(by='Followers', ascending=True)

# Create a bar chart for top followed artists in the selected country
fig_top_followed_artists_filtered = px.bar(top_followed_artists_filtered,
                                           x='Followers',
                                           y='Artist',
                                           orientation='h',
                                           labels={'Followers': 'Followers Count'},
                                           title=f'Top 10 Artists with Most Followers in {", ".join(country)}')

# Center the chart on the page
st.plotly_chart(fig_top_followed_artists_filtered)
st.markdown("""---""")
