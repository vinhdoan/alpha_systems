
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
# break in 6 months
for fileName in fileList:
    checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
    openingOrder = 0
    lastHigh = 0
    timesWon = 0
    timesLoss = 0
    #find entry pattern:
    #checkStock["52weeksHigh"] = pd.rolling_max(checkStock.High, window=252, min_periods=1)
    checkStock["2monthsHigh"] = checkStock.High.rolling(window=40, min_periods=1, center=False).max()
    #checkStock["48weeksHigh"] = checkStock.High.rolling(window=232, min_periods=1, center=False).max()
    checkStock["averageVol"] = checkStock.Volume.rolling(window=10, min_periods=1, center=False).min()
    if len(checkStock > 100):
        lastHigh = 0
        buyPrice = 0
        sellPrice = 0
        buyDate = datetime(2000, 1, 1)
        sellDate = datetime(2000, 1, 1)
        newOrder = pd.DataFrame(columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status'])
        i = 20
        while i < len(checkStock) - 10:
            if openingOrder == 0:
                if checkStock.ix[i]['Close'] <= 10 and checkStock.ix[i]['Close'] >= checkStock.ix[i - 1]['High'] and (
                    checkStock.ix[i]['Close'] > checkStock.ix[i-1]['2monthsHigh']) and   checkStock.ix[i]['Close'] >  checkStock.ix[i]['Open'] and checkStock.ix[i - 1][
                    'averageVol'] > 20000:
                    lastHigh = checkStock.ix[i - 1]['2monthsHigh']
                    buyPrice = checkStock.ix[i]['Close']
                    buyDate = checkStock.index[i]
                    total_orders += 1
                    openingOrder = 1
                    i = i + 4
                    continue
                else:
                    i = i + 1
            elif openingOrder == 1:
                if checkStock.ix[i]['High'] > buyPrice * 1.15:
                    sellPrice = checkStock.ix[i]['Close']
                    sellDate = checkStock.index[i]
                    percent = sellPrice/buyPrice - 1
                    win_orders += 1
                    openingOrder = 0
                    newOrder = pd.DataFrame([[fileName, buyDate, buyPrice, sellDate, sellPrice, 'won',percent]],
                                            columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status','percent'])
                    orders = pd.concat([orders, newOrder])
                    lastHigh = 0
                    buyPrice = 0
                    sellPrice = 0
                    buyDate = datetime(2000, 1, 1)
                    sellDate = datetime(2000, 1, 1)
                    timesWon += 1
                    if i < len(checkStock) - 25:
                        i = i + 22
                        continue
                    else:
                        break
                elif checkStock.ix[i]['Close'] <= buyPrice * 0.95:
                    sellPrice = checkStock.ix[i]['Close']
                    sellDate = checkStock.index[i]
                    percent = sellPrice/buyPrice - 1
                    loss_orders += 1
                    openingOrder = 0
                    newOrder = pd.DataFrame([[fileName, buyDate, buyPrice, sellDate, sellPrice, 'loss',percent]],
                                            columns=['stock', 'buyDate', 'buyPrice', 'sellDate', 'sellPrice', 'status','percent'])
                    orders = pd.concat([orders, newOrder])
                    lastHigh = 0
                    buyPrice = 0
                    sellPrice = 0
                    buyDate = datetime(2000, 1, 1)
                    sellDate = datetime(2000, 1, 1)
                    timesLoss += 1
                    if i < len(checkStock) - 25:
                        i = i + 22
                        continue
                    else:
                        break
                else:
                    i += 1
        if timesLoss > 0 or timesWon > 0:
            tempStats = pd.DataFrame([[fileName, timesWon, timesLoss, timesWon / (timesWon + timesLoss) * 100]],
                                     columns=['stock', 'won', 'loss', 'wonRate'])
            statistics = pd.concat([statistics, tempStats])

orders.to_csv('testresults/penny-breakout-2month-trades.csv', index=False)
statistics.to_csv('testresults/penny-breakout-2month-review.csv', index=False)
