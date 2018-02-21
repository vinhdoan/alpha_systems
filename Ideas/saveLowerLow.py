import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
from datetime import datetime, date
from scipy.signal import argrelextrema
from operator import itemgetter

checkStock = pd.read_csv('data/VNM.csv', index_col=0, parse_dates=['Date'])
minSeries = checkStock.ix[:, 3]
maxSeries = checkStock.ix[:,2]
a = argrelextrema(minSeries.values, np.less, order=1)
b = argrelextrema(maxSeries.values, np.less, order=1)
lowArray = a[0]
highArray = b[0]
lowerDayIndex = np.intersect1d(a, b)
if(len(lowerDayIndex>0)):
    lowerDayData = checkStock.ix[lowerDayIndex]
    #lowerDayData = lowerDayData.reset_index(drop=True)
    for i in range(len(checkStock)):
        checkStock.ix[i]['LL'] = lowerDayData.loc[lowerDayData.index<checkStock.ix[i]]
