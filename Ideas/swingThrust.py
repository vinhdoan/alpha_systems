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
        checkStock["6monthsLow"] = checkStock.Low.rolling(window=125, min_periods=1, center=False).min()
        if len(checkStock)>252:
            i = 0
            while i < len(checkStock)-10:
                if checkStock.ix[i]['Low'] < checkStock.ix[i-1]['6monthsLow'] and checkStock.ix[i+2]['High'] > checkStock.ix[i+1]['High'] >  checkStock.ix[i]['High'] and  checkStock.ix[i+2]['Low'] > checkStock.ix[i+1]['Low'] >  checkStock.ix[i]['Low']:
                    newOrder =  pd.DataFrame([[fileName,checkStock.index[i]]],columns=['stock', 'buyDate'])
                    orders = pd.concat([orders, newOrder])
                i+=1
    orders.to_csv('testresults/first-thrust-pattern.csv')
