import numpy as np
import os
import pandas as pd
from pandas_datareader import data as pdr

import matplotlib.pyplot as plt        
import statsmodels.api as sm

# strategy optimization giving a good Sharpe ratio
# Pair Trading of GLD and GDX
def catch_spread(excelname1, excelname2):
    df1=pd.read_excel(excelname1)
    df2=pd.read_excel(excelname2)
    
    #df1=pd.read_excel('ETH-USD.xlsx')
    #df2=pd.read_excel('BTC-USD.xlsx')
    df=pd.merge(df1, df2, on='Date', suffixes=('_GLD', '_GDX'))
    df.set_index('Date', inplace=True)
    df.sort_index(inplace=True)
    
    trainsetlength = 252
    trainset=np.arange(0, trainsetlength)
    testset=np.arange(trainset.shape[0], df.shape[0]) 
    
    model=sm.OLS(df.loc[:, 'Adj Close_GLD'].iloc[trainset],df.loc[:, 'Adj Close_GDX'].iloc[trainset])
    results=model.fit()
    hedgeRatio=results.params
    
    # spread=GLD - hedgeRatio*GDX
    spread=df.loc[:, 'Adj Close_GLD']-hedgeRatio[0]*df.loc[:, 'Adj Close_GDX']
    plt.plot(spread.iloc[trainset])
    plt.plot(spread.iloc[testset])
    spreadMean=np.mean(spread.iloc[trainset])
    print("spread mean: " + str(spreadMean)) # 0.05219623850035999
    spreadStd=np.std(spread.iloc[trainset])
    print("spread std: " + str(spreadStd)) # 1.944860873496509
    df['zscore']=(spread-spreadMean)/spreadStd
    df['positions_GLD_Long']=0
    df['positions_GDX_Long']=0
    df['positions_GLD_Short']=0
    df['positions_GDX_Short']=0
    df.loc[df.zscore>= 1, ('positions_GLD_Short', 'positions_GDX_Short')]=[-1, 1] # Short spread
    df.loc[df.zscore<=-1, ('positions_GLD_Long', 'positions_GDX_Long')]=[1, -1] # Buy spread
    df.loc[df.zscore<=0.5, ('positions_GLD_Short', 'positions_GDX_Short')]=0 # Exit short spread
    df.loc[df.zscore>=-0.5, ('positions_GLD_Long', 'positions_GDX_Long')]=0 # Exit long spread
    
    df.fillna(method='ffill', inplace=True) # ensure exist-ing positions are carried forward unless there is an exit signal
    positions_Long=df.loc[:, ('positions_GLD_Long', 'positions_GDX_Long')]
    positions_Short=df.loc[:, ('positions_GLD_Short', 'positions_GDX_Short')]
    positions=np.array(positions_Long)+np.array(positions_Short)
    positions=pd.DataFrame(positions)
    dailyret=df.loc[:, ('Adj Close_GLD', 'Adj Close_GDX')].pct_change()
    pnl=(np.array(positions.shift())*np.array(dailyret)).sum(axis=1)
    sharpeTrainset=np.sqrt(trainsetlength)*np.mean(pnl[trainset[1:]])/np.std(pnl[trainset[1:]])
    print("Sharpe of the train set: " + str(sharpeTrainset)) # 1.9182982282569077
    sharpeTestset=np.sqrt(trainsetlength)*np.mean(pnl[testset])/np.std(pnl[testset])
    print("Sharpe of the test set: " + str(sharpeTestset)) # 1.494313761833427
    plt.plot(np.cumsum(pnl[testset]))
    plt.show()
    # positions.to_pickle('example3_6_positions') 
