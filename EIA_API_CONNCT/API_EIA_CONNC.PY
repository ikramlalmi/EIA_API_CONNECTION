#Import libraries
import pandas  as pd
import requests
import asyncio
import aiohttp
import os
import time
from datetime import datetime, timedelta 
from States import My_states



def get_series_ids(): 
# """Defines the series Ids and return them"""
        #list to hold all the series IDs
        series_Ids=[]
        series_ID = "ELEC.SALES.{state}-ALL.M"

        for state in My_states:
            series_Ids.append(series_ID.format(state=state))
        return series_Ids     
        

def get_col_names():
#defines the column names and return them
        #list to hold the columns names
        col_Names=[]
        col_NAME = "{state}_Monthly_Sales"
        for state in My_states:
            col_Names.append(col_NAME.format(state=state))
        return col_Names

    
# Pull in data via EIA API
def pull_data(api_key, series_Ids, col_Names):
#     """
#     Initialize list -final_data- this is the final list that will store all the data from the json pull. 
#     Then we will use this list to concat into a pandas dataframe. 
#     """ 
    final_data = []
    for i in range(len(series_Ids)):
        url_api = 'http://api.eia.gov/series/?api_key=' + api_key +'&series_id=' + series_Ids[i]

        r = requests.get(url_api)
        json_data = r.json()

        if r.status_code == 200:
            print('Success!')
        else:
            print('Error')

        df = pd.DataFrame(json_data.get('series')[0].get('data'),
                          columns = ['Date', col_Names[i]])
        df.set_index('Date', drop=True, inplace=True)
        final_data.append(df)
        
    return final_data
        
        
def combining_data_df(final_data):
#     """combines all of the data frames into a single data frame and performs some data cleaning"""
        # Choose start and end dates
        startDate = '2009-01-01'
        endDate = '2022-07-01'
        # Combine all the data into one dataframe
        electric_sales = pd.concat(final_data, axis=1)
        # Create date as datetype
        electric_sales['Year'] = electric_sales.index.astype(str).str[:4]
        electric_sales['Month'] = electric_sales.index.astype(str).str[4:]
        electric_sales['Day'] = 1
        electric_sales['Date'] = pd.to_datetime(electric_sales[['Year','Month','Day']])
        electric_sales.set_index('Date',drop=True,inplace=True)
        electric_sales.sort_index(inplace=True)
        electric_sales = electric_sales[startDate:endDate]
        electric_sales = electric_sales.iloc[:,:50]
        return electric_sales




def main():
    # API Key from EIA
    api_key = 'N8vhvILu0oOxeKivkRZpnkiaEzMs2U2iLuraK5Ku'
    # Fetching the series ids. 
    series_ids = get_series_ids()
    # Fetching the columns names.
    col_names = get_col_names()
    final_data = pull_data(api_key, series_ids, col_names)
    df=combining_data_df(final_data)       
    df.head(30)
    df.to_csv( "electric_sales.csv", index=True)
        
if __name__ == '__main__':
     main()
