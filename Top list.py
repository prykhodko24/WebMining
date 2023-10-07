from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
url = "https://kworb.net/spotify/songs.html"
response = requests.get(url,verify=False).text

soup = BeautifulSoup(response)

song_list=[]
links = soup.find_all('tr')
for i in links:
    songs=i.find_all('div')
    for song in songs:
        song_list.append(song.text)

# Create a list of dictionaries where each dictionary represents a row of data
data = []

for i in song_list:
    if " - " in i:
        A= i.split(" - ")
        data.append({"singer": A[0], "song_name": A[1]})
df = pd.DataFrame(data)
sing_num=[]
for i in df["singer"].unique():
    sing_num.append({"singer": i, "number": len(df[df["singer"]==i])})
sing_num_df = pd.DataFrame(sing_num)

df_sorted = sing_num_df.sort_values(by="number", ascending=False)

df_sorted = df_sorted.reset_index(drop=True)
first_10_rows = df_sorted.head(10)
first_10_rows.to_excel("singer_num.xlsx")