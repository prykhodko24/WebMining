
import Functions
import datetime
import time
import os
url="https://kworb.net/spotify/artists.html"
a=Functions.getting_df(url)


today_date = datetime.date.today()
formatted_date = today_date.strftime("%d_%m_%Y")
country_folder_path = os.path.join(os.getcwd(), "Artist")
subfolder_name = str(formatted_date)
Functions.create_folder(country_folder_path,subfolder_name)

today_date = datetime.date.today()
formatted_date = today_date.strftime("%d_%m_%Y")
a.to_excel(f"Artist/{subfolder_name}/General.xlsx")