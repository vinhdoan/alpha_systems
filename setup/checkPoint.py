
import requests
import math
import time
from datetime import timedelta,date,datetime
import pandas as pd
import numpy as np
import json
import requests
from scipy.signal import argrelextrema
from operator import itemgetter

#update SL and current Price
# update equity
df = pd.read_csv('checkPoint/portfolio.csv',parse_dates=['Date'])
alertIndex = []
df = df.loc[df.Closed==0]
df = df.reset_index(drop=True)
stockList = df.Stock
stockList = stockList.drop_duplicates()
#update SL: last higherLow
#update TP:
historyEquity = pd.read_csv('checkPoint/historyEquity.csv')
td = date.today()
equity = 0
for i in range(len(df)):
    url = 'https://price-hcm04.vndirect.com.vn/priceservice/derivative/transactions/q=symbol:' + df.ix[i]['Stock']
    result = requests.get(url)
    if result.status_code == 200:
        jsonData = result.json()
        symbol = jsonData['symbol']
        if len(symbol) == 3:
            data = jsonData['data']
            if (len(data) > 0):
                data = sorted(data, key=itemgetter('time'))
                last = (data[len(data) - 1]['last'])
                df.loc[df['Stock']==df.ix[i]['Stock'], 'CurrentPrice'] = last
                buyPrice = (float)(df.ix[i]['BuyPrice'])
                volume = df.ix[i]['Volume']
                df.loc[df['Stock'] == df.ix[i]['Stock'], 'Fee'] = (0.0015 * (float)(buyPrice) + 0.0025 * last) * volume
                df.loc[df['Stock'] == df.ix[i]['Stock'], 'Upnl'] = (float)(last - buyPrice)*(float)(volume) - df.ix[i]['Fee']
                equity += (float)(volume) * last - df.ix[i]['Fee']
            #update last lowerLow
            checkStock = pd.read_csv('data/'+symbol+'.csv',parse_dates=['Date'])
            checkStock = checkStock.loc[checkStock['Date'] >= df.ix[i]['Date']]
            checkStock = checkStock.reset_index(drop=True)
            minSeries = checkStock.ix[:, 3]
            maxSeries = checkStock.ix[:,2]
            a = argrelextrema(minSeries.values, np.less, order=1)
            b = argrelextrema(maxSeries.values, np.less, order=1)
            lowArray = a[0]
            highArray = b[0]
            lowerDayIndex = np.intersect1d(a, b)
            if(len(lowerDayIndex>0)):
                lowerDayData = checkStock.ix[lowerDayIndex]
                lowerDayData = lowerDayData.reset_index(drop=True)
                stopLoss = lowerDayData.ix[len(lowerDayData)-1]['Low']
                if(stopLoss >= df.ix[i]['StopLoss']):
                    df.loc[df['Stock'] == df.ix[i]['Stock'], 'StopLoss'] = stopLoss
                    print(symbol,stopLoss)
currentEquity = pd.DataFrame([[td,equity]],columns=['Date','Equity'])
historyEquity = pd.concat([historyEquity,currentEquity])
historyEquity.to_csv('checkPoint/historyEquity.csv',index=False)
df.to_csv('checkPoint/' + str(datetime.today().date())+ '-portfolio.csv',index=False)
df.to_csv('checkPoint/last-portfolio.csv',index=False)
#calculate unrealized equity + PnL:


