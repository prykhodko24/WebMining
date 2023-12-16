import Functions

url="https://kworb.net/spotify/toplists.html"
a=Functions.getting_df(url)
a.to_excel(f"Top_years.xlsx")