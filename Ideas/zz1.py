
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import zigzag as zz

from pandas_datareader import get_data_yahoo


df = pd.read_csv('data/PHR.csv', index_col=0, parse_dates=['Date'])
df = df.ix[len(df)-252:len(df)-1]
df = df.reset_index(drop=True)
pivots = zz.peak_valley_pivots(df.Close.values, 0.05, -0.01)
ts_pivots = pd.Series(df.Close, index=df.index)
ts_pivots = ts_pivots[pivots != 0]
df.Close.plot()
ts_pivots.plot(style='g-o');
plt.show()

