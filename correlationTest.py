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

testSignal = pd.DataFrame(columns=['Stock','sharpe'])
# stockList = df.ix[:,0]
# stockList = stockList.drop_duplicates()
# toDate = datetime.today()
fileList = glob.glob('data/*.csv')
end = datetime.today() - timedelta(31)
start = end - timedelta(90)
listDF = pd.read_csv('sharpeRatio1month.csv')
c = np.array([])

# b = np.array()

for i in range(len(listDF)):
    fileName = listDF.ix[i]['Stock']
    checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
    checkStock = checkStock[start:end]
    # print(len(checkStock))
    if len(checkStock)==62:
        # a = np.asarray(checkStock.Close)
        # print(a.shape)
        # c = np.concatenate([c, checkStock.Close])
        # print(np.asarray(checkStock.Close))
        c = np.concatenate((c,np.asarray(checkStock.Close)))

# print(len(c))
d = (int)(len(c)/62)
e = np.reshape(c, (d,62))
# print(e)
corr = np.corrcoef(e)
print(corr)

#
# for fileName in fileList:
#     checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
#     checkStock = checkStock[start:end]
#     if len(checkStock) > 0 and checkStock.Volume.mean()>50000:
#         checkStock = checkStock.reset_index()
#         checkStock = checkStock.sort_values('Date')
#         daily = checkStock['Close'][1:].values / checkStock['Close'][:-1].values - 1
#         sharpeRatio = math.sqrt(250) * np.average(daily) / np.std(daily)
#         if sharpeRatio > 2:
#             item = pd.DataFrame([[fileName, sharpeRatio]], columns=['Stock', 'sharpe'])
#             testSignal = pd.concat([testSignal, item])
#
#
# testSignal.sort_values('sharpe',ascending=False)
# testSignal.to_csv('sharpeRatio1month.csv')
#

