'''
default output of alphas:
- a csv file includes buy date, buy price, sell date, sell price, pnl, status (won/lose)
- input parameters:
    .csv data
    . transaction cost: transaction fee + PIT
    . list of monitoring stock: suggestion: based on the
    . only trade stock that transaction value > 3,000,000  / day
'''
import numpy as np
import pandas as pd
from datetime import date, datetime, timedelta

def before_trading_days(stock, date):
    data = pd.read_csv('data/'+stock+'.csv')

def calculateTransactionFee(buyPrice,sellPrice):
    return buyPrice * 0.0015 + sellPrice * 0.0025


