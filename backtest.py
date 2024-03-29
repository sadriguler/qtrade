#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
import numpy as np
import os
import pandas as pd
from pandas_datareader import data as pdr

import matplotlib.pyplot as plt        
import statsmodels.api as sm

from exfunc import *
from numpy.linalg import inv
from strategies import catch_spread


if __name__ == "__main__":
    pair = ['BTC-USD', 'ETH-USD']
    for symbol in pair:
        filename = symbol + '.xlsx'
        if os.path.exists(filename):
            continue
        else:
            data = test_yfinance(symbol)
            data.to_excel(symbol+'.xlsx')
    
    # catch_spread('GLD.xls','GDX.xls')
    # This file was saved as epchan.com/book/example3_7.ipynb
    # Simple Mean-Reverting Model with and without Transaction Costs
    """
    startDate=20060101
    endDate=20061231
    # can be tested S&P400 mid-cap and S&P600 small-cap universes
    df=pd.read_table('SPX_op_20071123.txt')  
    df['Date']=df['Date'].astype('int')
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    dailyret=df.pct_change()
    marketDailyret=dailyret.mean(axis=1)
    weights=-(np.array(dailyret)-np.array(marketDailyret).reshape((dailyret.shape[0], 1)))
    wtsum=np.nansum(abs(weights), axis=1)
    weights[wtsum==0,]=0
    wtsum[wtsum==0]=1
    weights=weights/wtsum.reshape((dailyret.shape[0],1))
    dailypnl=np.nansum(np.array(pd.DataFrame(weights).shift())*np.array(dailyret), axis=1)
    dailypnl=dailypnl[np.logical_and(df.index >= startDate,df.index <= endDate)]    
    sharpeRatio=np.sqrt(252)*np.mean(dailypnl)/np.std(dailypnl)
    print('Sharpe ratio: ' + str(sharpeRatio)) #  0.957785681010386
    # With transaction costs
    onewaytcost=0.0005
    weights=weights[np.logical_and(df.index >= startDate,df.index <= endDate)]
    dailypnlminustcost=dailypnl - (np.nansum(abs(weights-np.array(pd.DataFrame(weights).shift())),axis=1)*onewaytcost)
    sharpeRatioMinusTcost=np.sqrt(252)*np.mean(dailypnlminustcost)/np.std(dailypnlminustcost)
    print('Sharpe ratio - cost: ' + str(sharpeRatioMinusTcost)) # -2.1617433718962276
    """
    
    # Calculating the Optimal Allocation Using Kelly formula
    df1=pd.read_excel('OIH.xls')    
    df2=pd.read_excel('RKH.xls')
    df=pd.merge(df1, df2, on='Date', suffixes=('_OIH', '_RKH'))
    df.set_index('Date', inplace=True)
    df3=pd.read_excel('RTH.xls')
    df=pd.merge(df, df3, on='Date')
    df.rename(columns={"Adj Close": "Adj Close_RTH"},inplace=True)
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    dailyret=df.loc[:, ('Adj Close_OIH', 'Adj Close_RKH','Adj Close_RTH')].pct_change()
    dailyret.rename(columns={"Adj Close_OIH": "OIH","Adj Close_RKH": "RKH", "Adj Close_RTH": "RTH"},inplace=True)
    excessRet=dailyret-0.04/252
    M=252*excessRet.mean()
    print('M: \n' + str(M))
    
    C=252*excessRet.cov()
    print('C: \n' + str(C))
    
    F=np.dot(inv(C), M)
    print('F: \n' + str(F))
    
    g=0.04+np.dot(F.T, np.dot(C, F))/2
    print('g: ' + str(g))
    
    S=np.sqrt(np.dot(F.T, np.dot(C, F)))
    print('S: ' + str(S))
    """print('First part of example')
    df=pd.read_excel('IGE.xls')
    df.sort_values(by='Date', inplace=True)
    dailyret=df.loc[:, 'Adj Close'].pct_change() # daily returns
    excessRet=dailyret-0.04/252 # excess daily returns = strategy returns - financing cost, assuming risk-free rate of
    sharpeRatio=np.sqrt(252)*np.mean(excessRet)/np.std(excessRet)
    print(sharpeRatio)
    
    print('Second part of example')
    df2=pd.read_excel('SPY.xls')
    df=pd.merge(df, df2, on='Date', suffixes=('_IGE', '_SPY'))
    df['Date']=pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    dailyret=df[['Adj Close_IGE', 'Adj Close_SPY']].pct_change() # daily returns
    dailyret.rename(columns={"Adj Close_IGE": "IGE", "Adj Close_SPY": "SPY"}, inplace=True)
    netRet=(dailyret['IGE']-dailyret['SPY'])/2
    sharpeRatio=np.sqrt(252)*np.mean(netRet)/np.std(netRet)
    print(sharpeRatio)
    
    cumret=np.cumprod(1+netRet)-1
    plt.plot(cumret)
    plt.show()
    
    maxDrawdown, maxDrawdownDuration, startDrawdownDay=calculateMaxDD(cumret.values)
    print(maxDrawdown) # -0.09529268047208683
    print(maxDrawdownDuration) # 497.0
    print(startDrawdownDay) # 1223
    """