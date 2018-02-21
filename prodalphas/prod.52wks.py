import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from datetime import datetime


fileList = glob.glob('data/*.csv')
orders = pd.DataFrame(columns=['stock','buyDate','buyPrice','sellDate','sellPrice','status'])
fileList = glob.glob('data/*.csv')
orders = pd.DataFrame(columns=['stock','buyDate','buyPrice','sellDate','sellPrice','status'])
statistics = pd.DataFrame(columns=['stock','won','loss','wonRate'])
total_orders = 0
win_orders = 0
loss_orders = 0
for fileName in fileList:
    checkStock = pd.read_csv(fileName, index_col=0, parse_dates=['Date'])
    #checkStock = checkStock.reset_index(drop=True)
    #find entry pattern:
    checkStock["52weeksHigh"] = checkStock.High.rolling(window=65, min_periods=1, center=False).max()
    checkStock["averageVol"] = checkStock.Volume.rolling(window=20, min_periods=1, center=False).mean()
    if len(checkStock)>252:
        for i in range(1,5):
            if (checkStock.ix[len(checkStock) - i]['Open'] >= checkStock.ix[len(checkStock) - i - 1]['Close'])  and checkStock.ix[len(checkStock) - i]['High'] >= \
                            checkStock.ix[len(checkStock) - i - 1]['High'] * 1.03 and (
                checkStock.ix[len(checkStock) - i]['High'] > checkStock.ix[len(checkStock) - i - 1]['52weeksHigh']) and checkStock.ix[len(checkStock) - i - 1][
                'averageVol'] > 30000:
                print(fileName,checkStock.index[len(checkStock)-i])
                break
                #len(checkStock) - i