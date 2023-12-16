import os
import pandas as pd
folder_path = '../top_2500'

# Get a list of all files in the folder
files = os.listdir(folder_path)
Country_df= pd.DataFrame()
for date in files:
    print(f"File: {date}")
    excel_path = f'{folder_path}/{date}'

    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_path)
    df['Date'] = date.split('.')[0]
    # Convert the 'date_column' to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d_%m_%Y')
    Country_df = pd.concat([Country_df, df], ignore_index=True)
Country_df = Country_df.drop(columns=['Unnamed: 0'])
print(Country_df.iloc[0])
Country_df.to_excel(f"Top_2500_total.xlsx")