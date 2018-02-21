import pandas as pd
import numpy as np
from _datetime import date,datetime

df = pd.read_csv('cafef_tx_history.csv',parse_dates=['date'])
stockList = df.Stock
stockList = stockList.drop_duplicates()
for stock in stockList:
    checkStock = df[df['Stock'].isin([stock])]
    checkStock = checkStock.reset_index(drop=True)
    checkStock = checkStock.sort_values('date')
    checkStock.to_csv('dataNN/'+stock+'.csv',index=False)

