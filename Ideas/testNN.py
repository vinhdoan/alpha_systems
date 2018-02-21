import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date, datetime

df = pd.read_csv('dataNN/BID.csv', parse_dates=['date'])
df['sum'] = df.net_val.rolling(window=20).sum()