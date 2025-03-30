from tefas import Crawler

from time import gmtime, strftime

import pandas as pd

def get_today():
    return strftime('%Y-%m-%d',gmtime())

def download_data(fund: str = 'MAC', market: str = 'TEFAS', start: str = '2025-01-01'):
    """
    Downloads the data from the related API for interested asset.
    
    Args: 
        fund: the interested asset
        market: the related market
        start: the start date of the asset history
        
    Returns:
        data: the requested data
        
    """
    tefas_data = Crawler()
    end_date  = strftime('%Y-%m-%d',gmtime())
    print(f'Downloading **{fund}** data from {market} for the dates {start}---{end_date}')
    data = tefas_data.fetch(start=str(start), end=end_date, name=fund, columns=["code", "date", "price", "stock", "number_of_investors"])
    print('Data was fetched from the API!')
    data = data.sort_values('date')
    data = data.reset_index(drop = True)
    if len(data) == 0:
        print(f'Nothing downloaded, be sure if nothing is wrong!')
    else:
        return data    

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
        data = download_data(fund = fund, market = market, start = '2025-01-01')
        
        filename = f'{market}_{fund}.pkl'
        data.to_pickle(filename)
        print(f'Data saved in {filename}')
    return data