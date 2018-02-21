import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import zigzag as zz

# from pandas_datareader import get_data_yahoo


df = pd.read_csv('data/ABT.csv', index_col=0, parse_dates=['Date'])
# df = df.ix[len(df)-70:len(df)]

df.rolling_std = df['Close'].rolling(5).std() * 10
df.change = df.rolling_std / df.Close

# pivots = zz.peak_valley_pivots(df.Close.values, 0.05, -0.01)
# ts_pivots = pd.Series(df.Close, index=df.index)
# ts_pivots = ts_pivots[pivots != 0]
ts_rolling = pd.Series(df.rolling_std,index=df.index)
ts_close = pd.Series(df.Close,index=df.index)
ts_rolling.plot();
ts_close.plot();
# df.rolling_std.plot()
# df.Close.plot()
# ts_pivots.plot(style='g-o');
plt.show()