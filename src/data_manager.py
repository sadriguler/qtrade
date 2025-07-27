from tefas import Crawler

from time import gmtime, strftime

import pandas as pd
import yfinance as yf

from datetime import date, timedelta
from src.config import YF_ASSET_NAMES

def days_between(date1_str, date2_str):
    """
    Source: Google-Gemini AI
    Calculates the number of days between two dates given as strings (YYYY-MM-DD).

    Args:
        date1_str: The first date as a string in 'YYYY-MM-DD' format.
        date2_str: The second date as a string in 'YYYY-MM-DD' format.

    Returns:
        An integer representing the number of days between the two dates.
        Returns None if the input date strings are invalid.
    """
    try:
        date1 = date.fromisoformat(date1_str)
        date2 = date.fromisoformat(date2_str)
        return abs((date2 - date1).days)
    except ValueError:
        return None

def find_date_after_days(start_date_str, num_days):
    """
    Source: Google-Gemini AI
    Finds the date that is a specified number of days after a given date.

    Args:
        start_date_str: The starting date as a string in 'YYYY-MM-DD' format.
        num_days: The number of days to add.

    Returns:
        A string representing the date after the specified number of days in 'YYYY-MM-DD' format.
        Returns None if the input date string is invalid.
    """
    try:
        start_date = date.fromisoformat(start_date_str)
        future_date = start_date + timedelta(days=num_days)
        return future_date.isoformat()
    except ValueError:
        return None

def get_today():
    return strftime('%Y-%m-%d',gmtime())

def download_data(asset: str = 'MAC', market: str = 'TEFAS', start: str = '2025-01-01'):
    """
    Downloads the data by using the related API for the interested asset.
    
    Args: 
        asset: the interested asset
        market: the related market
        start: the start date of the asset history
        
    Returns:
        data: the requested data
        
    """
    start = str(start)
    tefas_data = Crawler()
    end_date  = strftime('%Y-%m-%d',gmtime())
    data_list = []
    if market == "TEFAS":    
        while days_between(start, end_date) > 90:
            temporary_end_date = find_date_after_days(start, 90)
            data = tefas_data.fetch(start=start, end=temporary_end_date, name=asset, columns=["code", "date", "price", "stock", "number_of_investors"])
            data_list.append(data)
            start = find_date_after_days(temporary_end_date, 1)
            print(f"Downloading data from start: {start}, to temporary: {temporary_end_date}")
        else: 
            if days_between(start, end_date) > 1:
                data = tefas_data.fetch(start=start, end=end_date, name=asset, columns=["code", "date", "price", "stock", "number_of_investors"])
                data_list.append(data)
        print('Data was fetched from the API!')
        if len(data_list) > 1:
            for i, data in enumerate(data_list): 
                data_list[i] = data.sort_values('date').reset_index(drop = True)
            data = pd.concat(data_list).reset_index(drop = True)
            data['Date'] = pd.to_datetime(data['date'])
            data.drop(columns='date', inplace=True)
            return data
        elif len(data_list) == 1:
            if len(data_list[0]) == 0:
                print('ERROR: The requested data was not downloaded. There is a problem!')
                return 0
            else: 
                return data_list[0]
        else:   
            print('ERROR: The requested data was not downloaded. There is a problem!')
            return 0
    elif market == 'NYSE' or market == 'NASDAQ':
        data = yf.download(asset, period = 'max', auto_adjust=False, start=start)
        return data
    elif market == 'FOREX':
        if asset in YF_ASSET_NAMES:
            data = yf.download(YF_ASSET_NAMES[asset], period = 'max', auto_adjust=False, start=start)
        else:
            data = yf.download(YF_ASSET_NAMES[asset], period = 'max', auto_adjust=False, start=start)
        return data
    else: 
        print("I'm able to download data only from TEFAS!")
        
        

def get_data(fund: str = 'MAC', market: str = 'TEFAS'):
    filename = f'{market}_{fund}.pkl'
    try: # check if data exists
        # if exists, load the data
        data = pd.read_pickle(filename)
        number_of_elements = len(data)
        last_date_in_data = data.loc[number_of_elements - 1, 'date']
        today = get_today()
        if last_date_in_data == today:
            print('Data is up-to-date, returning the data for use!')
        else:
            print('Data is being updated...')
            recent_data = download_data(fund = fund, market = market, start = last_date_in_data)
            # only update the data if it has new information, because of weekends sometimes it is not updated!
            if len(recent_data) > 1: 
                recent_data = recent_data.sort_values('date')
                recent_data = recent_data.reset_index(drop = True)
                data = pd.concat([data, recent_data.loc[1,:]], ignore_index=True)
                
                filename = f'{market}_{fund}.pkl'
                print(f'Data saved in {filename}')
                data.to_pickle(filename)
            else: 
                return data
    except FileNotFoundError:
        print("The file does not exist; downloading the data...")   
        data = download_data(fund = fund, market = market, start = '2024-01-01')
        
        filename = f'{market}_{fund}.pkl'
        data.to_pickle(filename)
        print(f'Data saved in {filename}')
    return data