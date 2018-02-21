'''
price increases at least 90% in less than 2 months (44 candles)
then consolidated as

'''

'''
price reach 6 months low
then it has 2 consecutive higher low and higher high days
'''

if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    import scipy as sp
    import glob
    import datetime
    from datetime import datetime, date

    fileList = glob.glob('data/*.csv')
    orders = pd.DataFrame(columns=['stock', 'buyDate'])   # 'buyPrice', 'sellDate', 'sellPrice', 'status', 'percent'])
    statistics = pd.DataFrame(columns=['stock', 'won', 'loss', 'wonRate'])
    total_orders = 0
    win_orders = 0
    loss_orders = 0
    for fileName in fileList:
        checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
        openingOrder = 0
        lastHigh = 0
        timesWon = 0
        timesLoss = 0
        checkStock["2monthsLow"] = checkStock.Low.rolling(window=44, min_periods=1, center=False).min()
        checkStock["averageVol"] = checkStock.Volume.rolling(window=10, min_periods=1, center=False).min()
        if len(checkStock)>252:
            i = 0
            while i < len(checkStock)-25:
                if checkStock.ix[i]['High'] >= 1.9 * checkStock.ix[i-1]['2monthsLow'] and checkStock.ix[i-1]["averageVol"] > 20000 and checkStock.ix[i]['High'] >checkStock.ix[i+1]['Close'] and checkStock.ix[i]['High'] >checkStock.ix[i+2]['Close']  :
                    newOrder =  pd.DataFrame([[fileName,checkStock.index[i]]],columns=['stock', 'buyDate'])
                    orders = pd.concat([orders, newOrder])
                i+=20
    orders.to_csv('testresults/flag-high-and-tight.csv')
