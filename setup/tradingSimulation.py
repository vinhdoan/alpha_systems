import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt

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


df = pd.read_csv('testresults/test15.csv',parse_dates=['buyDate','sellDate'])
startDate = date(2017,1,1)
endDate = date(2017,10,1)

currDate = startDate
currentOrders = 0
funds = 1000.0
tempFund = funds
equityHistory = []
tradeDates = []
tradeHistory = pd.DataFrame(columns=['stt','buyDate','buyPrice','sellDate','sellPrice','status', 'equity'])
while currDate<endDate:
    condition = df['buyDate'] > currDate
    trade = df.loc[condition].iloc[0]
    if len(trade) == 7 and trade.sellPrice > 0 and trade.buyPrice > 0: #and currDate.strftime("%b") != 'Jul' and currDate.strftime("%b") != 'Mar':
        # bet full account
        tempFund = tempFund * (trade.sellPrice*0.9975) / (trade.buyPrice*1.0015)
        # bet 1/3 account
        #tempFund = 2/3*tempFund + 1/3*tempFund * (trade.sellPrice*0.9975) / (trade.buyPrice*1.0015)
        #tempFund = tempFund * (trade.sellPrice) / (trade.buyPrice)
        currDate = trade.sellDate.date()
        equityHistory.append(tempFund)
        tradeDates.append(trade.buyDate)
        trade['equity'] = tempFund
        tradeHistory = tradeHistory.append(trade)
    else:
        currDate = currDate + timedelta(10)

tradeHistory.to_csv('testresults/tradeHistory2017.csv')

#tradeHistory['Cumlative'] = tradeHistory['equity'] / tradeHistory['equity'][0]
#np.sqrt(N) * returns.mean() / returns.std()
print(max_drawdown(np.array(tradeHistory['equity'])))

plt.plot(tradeDates,equityHistory)
plt.show()
