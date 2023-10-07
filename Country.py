from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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

    response = requests.get(url_c, verify=False).text
    print(response)

