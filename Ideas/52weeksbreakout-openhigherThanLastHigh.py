# Entry rules:
#
# 	* (t-1 -> t-6)Breakout 52 weeks and open above the highest of last bar
# 	* Buy limit at lowest of breakout bar
#
# Exit rules:
#
# 	* Profit 15%
# 	* Price touch the last zone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
from datetime import datetime, date


fileList = glob.glob('data/*.csv')
orders = pd.DataFrame(columns=['stock','buyDate','buyPrice','sellDate','sellPrice','status'])
statistics = pd.DataFrame(columns=['stock','won','loss','wonRate'])
total_orders = 0
win_orders = 0
loss_orders = 0


for fileName in fileList:
    checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
    openingOrder = 0
    lastHigh = 0
    timesWon = 0
    timesLoss = 0
    #find entry pattern:
    #checkStock["52weeksHigh"] = pd.rolling_max(checkStock.High, window=252, min_periods=1)
    checkStock["52weeksHigh"] = checkStock.High.rolling(window=252,min_periods=1,center=False).max()
    #heckStock["47weeksHigh"] = checkStock.High.rolling(window=232, min_periods=1, center=False).max()
    checkStock["averageVol"] = checkStock.Volume.rolling(window=20, min_periods=1, center=False).mean()
    if len(checkStock>252):
        lastHigh = 0
        buyPrice = 0
        sellPrice = 0
        buyDate = datetime(2000,1,1)
        sellDate = datetime(2000,1,1)
        newOrder = pd.DataFrame(columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
        i = 252
        while i < len(checkStock)-10:
            if openingOrder==0:
                if (checkStock.ix[i]['Open'] > checkStock.ix[i-1]['High']) and checkStock.ix[i]['Close'] >= checkStock.ix[i-1]['Open'] * 1.03 and (checkStock.ix[i]['High'] > checkStock.ix[i-1]['52weeksHigh'])  and checkStock.ix[i-1]['averageVol']>50000:
                    lastHigh = checkStock.ix[i-1]['52weeksHigh']
                    buyPrice = checkStock.ix[i]['Close']
                    buyDate = checkStock.index[i]
                    total_orders += 1
                    openingOrder = 1
                    i=i+4
                    continue
                else:
                    i = i+1
            elif openingOrder==1:
                if checkStock.ix[i]['High'] > buyPrice*1.154:
                    sellPrice = buyPrice*1.15
                    sellDate = checkStock.index[i]
                    win_orders += 1
                    openingOrder = 0
                    newOrder = pd.DataFrame([[fileName,buyDate,buyPrice,sellDate,sellPrice,'won']],columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
                    orders = pd.concat([orders,newOrder])
                    lastHigh = 0
                    buyPrice = 0
                    sellPrice = 0
                    buyDate = datetime(2000,1,1)
                    sellDate = datetime(2000,1,1)
                    timesWon += 1
                    if i < len(checkStock) - 25:
                        i = i+1
                        continue
                    else:
                        break
                elif checkStock.ix[i]['Low']<buyPrice*0.954:
                    sellPrice = buyPrice*0.95
                    sellDate = checkStock.index[i]
                    loss_orders+=1
                    openingOrder = 0
                    newOrder = pd.DataFrame([[fileName, buyDate, buyPrice, sellDate, sellPrice, 'loss']],
                                            columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
                    orders = pd.concat([orders, newOrder])
                    lastHigh = 0
                    buyPrice = 0
                    sellPrice = 0
                    buyDate = datetime(2000,1,1)
                    sellDate = datetime(2000,1,1)
                    timesLoss+=1
                    if i < len(checkStock) - 25:
                        i = i+10
                        continue
                    else:
                        break
                else:
                    i += 1
        if timesLoss > 0 or timesWon > 0:
            tempStats = pd.DataFrame([[fileName,timesWon,timesLoss,timesWon/(timesWon+timesLoss)*100]],columns=['stock','won','loss','wonRate'])
            statistics = pd.concat([statistics,tempStats])

orders.to_csv('testresults/52weeksbreakout-buyt0Close15percentwithFee.csv')
statistics.to_csv('testresults/52weeksbreakoutStats-buyt0Close15percentwithFee.csv')




