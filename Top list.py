
import Functions
import datetime

url = "https://kworb.net/spotify/songs.html"
a=Functions.getting_df(url)

a['Artist']=[a['Artist and Title'][i].split(' - ')[0] for i in a.index]
a['Title']=[a['Artist and Title'][i].split(' - ')[1] for i in a.index]
today_date = datetime.date.today()
formatted_date = today_date.strftime("%d_%m_%Y")
a.to_excel(f"top_2500/{formatted_date}.xlsx")