from datetime import date, timedelta, datetime
import wget
import os
import zipfile
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import glob
import operator
import math
from random import randint

s = dict()
dataframes = dict()
# get the whole dataset
# fileList = glob.glob('data/Vietnam/*.csv')
#testSignal = pd.DataFrame(columns=['Stock','Date','buyPrice','stoploss','target','percentRisk','status','profit'])


# any close that is > 2 * stdeviation is outliner -> removed
# IQR -> removed
testSignal = pd.DataFrame(columns=['Stock','sharpe'])
# stockList = df.ix[:,0]
# stockList = stockList.drop_duplicates()
# toDate = datetime.today()
fileList = glob.glob('data/*.csv')
end = datetime.today()
start = end - timedelta(250)
for fileName in fileList:
    checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
    checkStock = checkStock[start:end]
    if len(checkStock) > 0 and checkStock.Volume.mean()>100000:
        checkStock = checkStock.reset_index()
        checkStock = checkStock.sort_values('Date')
        daily = checkStock['Close'][1:].values / checkStock['Close'][:-1].values - 1
        sharpeRatio = math.sqrt(250) * np.average(daily) / np.std(daily)
        if sharpeRatio > 2:
            item = pd.DataFrame([[fileName, sharpeRatio]], columns=['Stock', 'sharpe'])
            testSignal = pd.concat([testSignal, item])

testSignal.sort_values('sharpe',ascending=False)
testSignal.to_csv('sharpeRatio1year.csv')


