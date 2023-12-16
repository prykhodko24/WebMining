import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import os
def getting_df(url):
    response = requests.get(url, verify=False).text
    soup = BeautifulSoup(response)
    links = soup.find_all('tr')
    a = links[0].find_all('th')
    title = []
    for k in a:
        title.append(k.text)
    lst=[]
    for i in links[1:]:
        a=i.find_all('td')
        lst1 = []
        for k in a:
            lst1.append(k.text)
        lst.append(lst1)
    df = pd.DataFrame(lst, columns=title)
    return df

def create_folder(country_folder_path,subfolder_name):
    subfolder_path = os.path.join(country_folder_path, subfolder_name)
    try:
        os.makedirs(subfolder_path)
    except:
        print("We already have this folder")