from bs4 import BeautifulSoup
import requests
import Functions
import datetime
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

today_date = datetime.date.today()
formatted_date = today_date.strftime("%d_%m_%Y")
country_folder_path = os.path.join(os.getcwd(), "Country")
subfolder_name = str(formatted_date)
Functions.create_folder(country_folder_path,subfolder_name)

# Suppress the InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
url = "https://kworb.net/spotify/"
response = requests.get(url,verify=False).text

soup = BeautifulSoup(response)

country_list=[]
links = soup.find_all('tr')
for i in links:
    county_name = i.find('td',class_="mp text").text
    a = i.find('a')
    lnk=str(a).split('<a href="')[1].split('">Daily</a>')
    country_list.append([county_name,lnk[0]])

for cntr in country_list:
    url_c=url+cntr[1]
    try:
        a=Functions.getting_df(url_c)
        a.to_excel(f"Country/{subfolder_name}/{cntr[0]}.xlsx")
    except:
        print("ERROR",cntr[0])



