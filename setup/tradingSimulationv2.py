import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import math

def max_dd(ser):
    max2here = pd.expanding_max(ser)
    dd2here = ser - max2here
    return dd2here.min()

def max_drawdown(X):
    mdd = 0
    peak = X[0]
    for x in X:
        if x > peak:
            peak = x
        dd = (peak - x) / peak
        if dd > mdd:
            mdd = dd
    return mdd

def sharpeRatio(equityHistory,dateHistory, startDate, startFund):
    dailyRets = []
    lastUpdateDate = startDate
    tempRet = 0
    lastFund = 0
    lastPeriod = 0
    if len(equityHistory) == len(dateHistory):
        for i in range(len(equityHistory)):
            delta = dateHistory[i].date() - startDate
            deltadays = int(delta.days)
            if deltadays>0:
                lastPeriod = deltadays
                lastUpdateDate = startDate
                lastFund = startFund
                startDate = dateHistory[i].date()
                tempRet = equityHistory[i]/startFund
                tempDailyRet = tempRet**(1.0/float(deltadays)) - 1
                startFund = equityHistory[1]
                for j in range(deltadays):
                    dailyRets.append(tempDailyRet)
            else:
                tempRet = equityHistory[i]/lastFund
                tempDailyRet = tempRet**(1.0/float(lastPeriod)) - 1
                startFund = equityHistory[1]
                for j in range(deltadays):
                    dailyRets.append(tempDailyRet)
    sharpe =  math.sqrt(252) * np.average(dailyRets) / np.std(dailyRets)
    return sharpe

stats = pd.DataFrame(columns=['year','noOrders','Sharpe','maxDD','returns','maxdd/ret'])
dataset = pd.read_csv('testresults/52wksbreakout-buySellClose-15percent.csv',parse_dates=['buyDate','sellDate'])
#startDate = date(2016,10,1)
#endDate = date(2017,10,1)
startYear = 2010

for year in range(8):
    startDate = date(int(startYear)+year,1,1)
    endDate = date(int(startYear)+year,12,31)
    currDate = startDate
    for maxCurrentOrders in range(1,11):
        currentOrders = 0
        funds = 1000.0
        tempFund = funds
        equityHistory = []
        tradeDates = []
        tradeHistory = pd.DataFrame(columns=['stt','buyDate','buyPrice','sellDate','sellPrice','status', 'equity'])
        tempTrade = pd.DataFrame(columns=['stt','buyDate','buyPrice','sellDate','sellPrice','status'])
        df = dataset.loc[(dataset['buyDate']>startDate) & (dataset['sellDate']<endDate)]
        df = df.reset_index(drop=True)
        for i in range(len(df)):
            if len(tempTrade)<maxCurrentOrders:
                # 2 cases here:
                tempTrade = tempTrade.append(df.ix[i])
                tempTrade = tempTrade.sort_values('sellDate')
                tempTrade = tempTrade.reset_index(drop=True)
            else:
                # if previous orders can close, then close, add new orders, recalculate the funds
                if df.ix[i]['buyDate'] > tempTrade.ix[0]['sellDate']:
                    #close first tempTrade
                    trade = tempTrade.ix[0]
                    #pnl = 2*tempFund*trade.sellPrice/maxCurrentOrders/(trade.buyPrice) - 2*tempFund/maxCurrentOrders
                    #no margin:
                    volume = tempFund / maxCurrentOrders / trade.buyPrice
                    pnl = volume * trade.sellPrice - tempFund/maxCurrentOrders
                    #pnl = tempFund * trade.sellPrice / maxCurrentOrders / trade.buyPrice - tempFund / maxCurrentOrders
                    #tempFund = (maxCurrentOrders-1) * tempFund /maxCurrentOrders + (1/maxCurrentOrders) * tempFund * (trade.sellPrice*0.9975) / (trade.buyPrice*1.0015)
                    tempFund = tempFund + pnl
                    equityHistory.append(tempFund)
                    tradeDates.append(tempTrade.ix[0].sellDate)
                    trade['equity'] = tempFund
                    tradeHistory = tradeHistory.append(trade)
                    tempTrade.loc[0] = df.ix[i]
                    tempTrade = tempTrade.sort_values('sellDate')
                    tempTrade = tempTrade.reset_index(drop=True)
                else:
                    i = i+1
        #close the rest
        for k in range(len(tempTrade)):
            trade = tempTrade.ix[k]
            # pnl = 2 * tempFund * trade.sellPrice * 0.9975 / maxCurrentOrders / (
            # trade.buyPrice * 1.0015) - 2 * tempFund / maxCurrentOrders
            volume = tempFund / maxCurrentOrders / trade.buyPrice
            pnl = volume * trade.sellPrice - tempFund / maxCurrentOrders
            # tempFund = (maxCurrentOrders-1) * tempFund /maxCurrentOrders + (1/maxCurrentOrders) * tempFund * (trade.sellPrice*0.9975) / (trade.buyPrice*1.0015)
            tempFund = tempFund + pnl
            equityHistory.append(tempFund)
            tradeDates.append(trade.sellDate)
            trade['equity'] = tempFund
            tradeHistory = tradeHistory.append(trade)
        #tradeHistory.to_csv('testresults/tradereview-',maxCurrentOrders,'.csv')
        #tradeHistory['Cumlative'] = tradeHistory['equity'] / tradeHistory['equity'][0]
        #np.sqrt(N) * returns.mean() / returns.std()
        dd = max_drawdown(np.array(tradeHistory['equity']))
        #print(equityHistory)
        #sharpe = sharpeRatio(equityHistory,tradeDates,startDate,funds)
        #print(dd)
        #print(tempFund)
        print(int(startYear)+year)
        stats.loc[year*10+maxCurrentOrders-1] = [int(startYear)+year,maxCurrentOrders,0,dd,tempFund,float(tempFund/dd/10000)]
        #print("no orders",maxCurrentOrders,"sharpeRatio",sharpe,"max_drawdonw",dd,tempFund,float(tempFund/dd/10000))
        #plt.plot(tradeDates,equityHistory)
        #plt.show()

stats.to_csv('statistics-review-buysellClose15percent.csv')
print(stats)