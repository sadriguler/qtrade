from pandas import Timestamp as Timestamp
from pandas import DataFrame as DataFrame
from datetime import datetime

def add_a_row_to_transaction_history(date: Timestamp,  asset: str, market: str, position: str, amount: float, house: str, comment: str, transaction_history: DataFrame):
    """
    Adds the new operation to the transaction history. The inputs should be aligned with the transaction history as specificied 
    in the function description of define_empty_transaction_history().
    
    Args:
        Date: date of the transaction
        asset: equity type, i.e. TRY, USD, stocks, etc.
        net_change: nominal value of the change
        house: brokerage house
        comment: comments regarding the transaction
    
    Returns: 
        transaction_history: updated transaction_history
        
    Example usage: 
        transaction_history = add_a_row_to_transaction_history(date = date_to_pd_timestamp(day = 8, month = 1, year = 25), 
                                                                asset = 'TRY', 
                                                                net_change= 7000,
                                                                house = 'isbank',
                                                                comment = 'some savings',
                                                                transaction_history = transaction_history
                                                                )
    
    """
    
    new_row = { 
            'Date': date,
            'asset': asset, 
            'market' : market,
            'position' : position,
            'amount' : amount,
            'house': house, 
            'comment': comment,
            }    
    transaction_history.loc[len(transaction_history)] = new_row
    return transaction_history.sort_values('Date')


def calculate_interest_daily_return(amount: float, interest_rate: float, tax_rate: float, number_of_days: float):
    """
    Computes the daily return for given interesst and tax rates
    
    Args:
        amount: the net amount ot apply the interest
        interest_rate: the interest rate by the house, for 33%, it should be 0.33
        tax_rate: the tax rate cut, for 10%, it should be 0.10
        number_of_days: number of the days to apply the interest rate
    
    Returns: 
        net_return: net return of the interest on the holding amount after the tax cat 
        
    Example usage: 
        display(calculate_interest_daily_return(10_000, 0.33, 0.10, 1))
    """
    
    interest = round((amount*interest_rate/365*number_of_days)*100)/100
    tax_cut = round(interest*tax_rate*100)/100
    net_return = round((interest  - tax_cut)*100)/100
    return net_return

def date_to_pd_timestamp(day: int, month: int, year: int):
    """
    Returns pd.Timestamp for a given date. Time hour, monutes, and seconds of the returned timestamp are 0.
    
    Args: 
        day: day
        month: month
        year: year, for example: for 2025, it is 25
    
    Returns: 
        pd.Timestamp(day/month/year 00:00:00)
        
    Example usage:
        date_to_pd_timestamp(7, 1, 25)
    
    """
    return Timestamp(datetime.strptime(f'{day}/{month}/{year} 00:00:00','%d/%m/%y %H:%M:%S'))

def define_empty_transaction_history():
    """
    Defines an empty pd.Dataframe for recording transaction histories.
    
    Args:
    
    Returns:
        pd.DataFrame with columns of Date, asset, net_change, house, comment
            Date: date of the transaction
            asset: equity type, i.e. TRY, USD, stocks, etc.
            net_change: nominal value of the change
            house: brokerage house
            comment: comments regarding the transaction
    
    Example usage: 
        transaction_history = define_empty_transaction_history()
    
    """
    return DataFrame(columns=['Date','asset', 'market', 'amount', 'position', 'house','comment'])

