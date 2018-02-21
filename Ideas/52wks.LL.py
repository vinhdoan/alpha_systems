# Entry rules:
#
# 	* (t-1 -> t-6)Breakout 52 weeks and open above the highest of last bar
# 	* Buy limit at lowest of breakout bar
#
# Exit rules:
#
# 	* double top or lower low
# 	* Price touch the last zone
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
from datetime import datetime, date
from scipy.signal import argrelextrema
from operator import itemgetter


if __name__ == '__main__':
    fileList = glob.glob('data/*.csv')
    orders = pd.DataFrame(columns=['stock','buyDate','buyPrice','sellDate','sellPrice','status'])
    statistics = pd.DataFrame(columns=['stock','won','loss','wonRate'])
    total_orders = 0
    win_orders = 0
    loss_orders = 0
    for fileName in fileList:
        print(fileName)
        checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
        openingOrder = 0
        lastHigh = 0
        timesWon = 0
        timesLoss = 0
        #find entry pattern:
        #checkStock["52weeksHigh"] = pd.rolling_max(checkStock.High, window=252, min_periods=1)
        checkStock["52weeksHigh"] = checkStock.High.rolling(window=252,min_periods=1,center=False).max()
        checkStock["averageVol"] = checkStock.Volume.rolling(window=10, min_periods=1, center=False).mean()
        minSeries = checkStock.ix[:, 2]
        maxSeries = checkStock.ix[:, 1]
        a = argrelextrema(minSeries.values, np.less, order=1)
        b = argrelextrema(maxSeries.values, np.less, order=1)
        lowArray = a[0]
        highArray = b[0]
        if len(checkStock>252):
            lastHigh = 0
            buyPrice = 0
            sellPrice = 0
            stopLoss = 0
            buyDate = datetime(2000,1,1)
            sellDate = datetime(2000,1,1)
            newOrder = pd.DataFrame(columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
            i = 200
            while i < len(checkStock)-10:
                if openingOrder==0:
                    if checkStock.ix[i]['Close']>= checkStock.ix[i]['Open'] > checkStock.ix[i-1]['High']and (checkStock.ix[i]['High'] >= checkStock.ix[i-1]['52weeksHigh']*1.03) and checkStock.ix[i-1]['averageVol']>30000:
                        lastHigh = checkStock.ix[i-1]['52weeksHigh']
                        buyPrice = checkStock.ix[i]['Close']
                        buyDate = checkStock.index[i]
                        total_orders += 1
                        openingOrder = 1
                        stopLoss = buyPrice * 0.95
                        i=i+4
                        continue
                    else:
                        i = i+1
                elif openingOrder==1:
                    # find lowerLow
                    if checkStock.ix[i]['High'] < checkStock.ix[i + 1]['High'] and checkStock.ix[i]['High'] < \
                            checkStock.ix[i - 1]['High'] and checkStock.ix[i]['Low'] < checkStock.ix[i + 1]['Low'] and \
                                    checkStock.ix[i]['Low'] < checkStock.ix[i - 1]['Low'] and checkStock.ix[i]['Close'] > stopLoss:
                        stopLoss = checkStock.ix[i]['Low']
                        i = i+2
                    elif checkStock.ix[i]['Close'] <= stopLoss:
                        # check lowerLow, higherHig
                        sellPrice = checkStock.ix[i]['Close']
                        sellDate = checkStock.index[i]
                        status = ''
                        if sellPrice>buyPrice:
                            win_orders += 1
                            status = 'won'
                        else:
                            loss_orders +=1
                            status = 'loss'
                        openingOrder = 0
                        newOrder = pd.DataFrame([[fileName,buyDate,buyPrice,sellDate,sellPrice,status]],columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
                        orders = pd.concat([orders,newOrder])
                        buyDate = datetime(2000,1,1)
                        sellDate = datetime(2000,1,1)
                        timesWon += 1
                        if i < len(checkStock) - 25:
                            i = i+22
                            continue
                        else:
                            break
                    else:
                        i += 1
            if timesLoss > 0 or timesWon > 0:
                tempStats = pd.DataFrame([[fileName,timesWon,timesLoss,timesWon/(timesWon+timesLoss)*100]],columns=['stock','won','loss','wonRate'])
                statistics = pd.concat([statistics,tempStats])

    orders.to_csv('testresults/52wksbreakout-doubleTop-lowerLow-trades.csv',index=False)
    #statistics.to_csv('testresults/52wksbreakoutstats-doubleTop-lowerLow-statistics.csv',index=False)




