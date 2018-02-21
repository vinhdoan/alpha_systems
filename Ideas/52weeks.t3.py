# Entry rules:
#
# 	* (t-1 -> t-6)Breakout 52 weeks and open above the highest of last bar
# 	* Buy limit at lowest of breakout bar
#
# Exit rules:
#
# 	* Profit 15%
# 	* Price touch the last zone


# result is not really good, need time for price to increaes

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from datetime import datetime

fileList = glob.glob('data/*.csv')
orders = pd.DataFrame(columns=['stock','buyDate','buyPrice','sellDate','sellPrice','status','percent'])
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
    checkStock["averageVol"] = checkStock.Volume.rolling(window=20, min_periods=1, center=False).mean()
    if len(checkStock>252):
        lastHigh = 0
        buyPrice = 0
        sellPrice = 0
        buyDate = datetime(2000,1,1)
        sellDate = datetime(2000,1,1)
        newOrder = pd.DataFrame(columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status','percent'])
        i = 126
        while i < len(checkStock)-10:
            #if openingOrder==0:
            if (checkStock.ix[i]['Open'] > checkStock.ix[i-1]['High']) and (checkStock.ix[i]['Open'] > checkStock.ix[i-1]['52weeksHigh']) and checkStock.ix[i-1]['averageVol']>50000:
                lastHigh = checkStock.ix[i-1]['52weeksHigh']
                buyPrice = checkStock.ix[i]['Close']
                buyDate = checkStock.index[i]
                sellPrice = checkStock.ix[i+3]['Open']
                sellDate = checkStock.index[i+3]
                percent = (sellPrice - buyPrice)/buyPrice
                if sellPrice>buyPrice*1.03:
                    status = 'won'
                    timesWon += 1
                else:
                    status = 'lose'
                    timesLoss += 1
                total_orders += 1
                newOrder = pd.DataFrame([[fileName, buyDate, buyPrice, sellDate, sellPrice, status,percent]],
                                        columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status','percent'])
                orders = pd.concat([orders, newOrder])
                i=i+20
                lastHigh = 0
                buyPrice = 0
                sellPrice = 0
                buyDate = datetime(2000, 1, 1)
                sellDate = datetime(2000,1,1)
            else:
                i = i+1
        #     elif openingOrder==1:
        #         if checkStock.ix[i]['High'] > buyPrice*1.15:
        #             sellPrice = buyPrice*1.15
        #             sellDate = checkStock.index[i]
        #             win_orders += 1
        #             openingOrder = 0
        #             newOrder = pd.DataFrame([[fileName,buyDate,buyPrice,sellDate,sellPrice,'won']],columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
        #             orders = pd.concat([orders,newOrder])
        #             lastHigh = 0
        #             buyPrice = 0
        #             sellPrice = 0
        #             buyDate = datetime(2000,1,1)
        #             sellDate = datetime(2000,1,1)
        #             timesWon += 1
        #             if i < len(checkStock) - 25:
        #                 i = i+22
        #                 continue
        #             else:
        #                 break
        #         elif checkStock.ix[i]['Low']<buyPrice*0.95:
        #             sellPrice = buyPrice*0.95
        #             sellDate = checkStock.index[i]
        #             loss_orders+=1
        #             openingOrder = 0
        #             newOrder = pd.DataFrame([[fileName, buyDate, buyPrice, sellDate, sellPrice, 'loss']],
        #                                     columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
        #             orders = pd.concat([orders, newOrder])
        #             lastHigh = 0
        #             buyPrice = 0
        #             sellPrice = 0
        #             buyDate = datetime(2000,1,1)
        #             sellDate = datetime(2000,1,1)
        #             timesLoss+=1
        #             if i < len(checkStock) - 25:
        #                 i = i+22
        #                 continue
        #             else:
        #                 break
        #         else:
        #             i += 1
        # if timesLoss > 0 or timesWon > 0:
        #     tempStats = pd.DataFrame([[fileName,timesWon,timesLoss,timesWon/(timesWon+timesLoss)*100]],columns=['stock','won','loss','wonRate'])
        #     statistics = pd.concat([statistics,tempStats])

orders.to_csv('testresults/52weekst3.csv')
#statistics.to_csv('testresults/52weeksbreakoutStats.csv')




