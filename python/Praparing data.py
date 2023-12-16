import os
import pandas as pd
from API import search_for_artist
folder_path = '../Country'

# Get a list of all files in the folder
files = os.listdir(folder_path)
Country_df= pd.DataFrame()
for date in files:
    print(f"File: {date}")
    folder_path = f'Country/{date}'

    countries = os.listdir(folder_path)
    for country in countries:
        print(f"Country: {country}")
        excel_path = f'Country/{date}/{country}'

        # Read the Excel file into a DataFrame
        df = pd.read_excel(excel_path)
        df['Date'] = date
        # Convert the 'date_column' to datetime
        df['Date'] = pd.to_datetime(df['Date'], format='%d_%m_%Y')
        df['Country']=country.split(".")[0]
        Country_df = pd.concat([Country_df, df], ignore_index=True)
print(Country_df)
        # Display the DataFrame
Country_df = Country_df.drop(columns=['Unnamed: 0'])
Country_df["Artist"]=(Country_df['Artist and Title'].str.split(' - ',expand=True))[0]
Country_df["Title"]=(Country_df['Artist and Title'].str.split(' - ',expand=True))[1]
cont = pd.read_excel('country_cont.xlsx')
cont = cont.drop(columns=['Unnamed: 2'])
Country_df = pd.merge(Country_df, cont, on='Country', how='left')
art_xls = pd.read_excel('art_order - Copy.xlsx')
art_xls = art_xls.dropna(subset=['Followers'])
# art_lst=list(art_xls['Artist'])
# art_lst=list(art_xls['Followers'])
art_lst=list(art_xls['Artist'])

artist_df= pd.DataFrame()
artist_df["Artist"]=list(set(Country_df["Artist"]))
artist_df["Followers"]=''
artist_df["Genres"]=''
artist_df["Popularity"]=''
artist_df["Images"]=''
artist_df.to_excel('art_order.xlsx', index=False)
for i in range(len(artist_df)):

    if artist_df["Artist"][i] in art_lst:
        print("cont")
        continue
    try:
        res = (search_for_artist(artist_df["Artist"][i]))

        artist_df.loc[i, 'Followers'] = res['artists']['items'][0]['followers']['total']
        artist_df.loc[i, 'Genres'] = (', '.join(res['artists']['items'][0]['genres']))
        artist_df.loc[i, 'Images'] = (res['artists']['items'][0]['images'][0]['url'])
        artist_df.loc[i, 'Popularity'] = (res['artists']['items'][0]['popularity'])
        artist_df.to_excel('art_order.xlsx', index=False)
    except:
        print(artist_df["Artist"][i])
artist_df=artist_df[artist_df['Followers']!='']
artist_df = pd.concat([artist_df, art_xls], ignore_index=True)

result_df = pd.merge(Country_df, artist_df, on='Artist', how='left')
country_df_filtered = result_df[result_df['Followers'] != '']
country_df_filtered.to_excel('Country_total.xlsx', index=False)
artist_df.to_excel('art_order.xlsx', index=False)