import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from datetime import datetime

df = pd.read_csv('testresults/52weeksbreakout-buyt0Close20percent.csv',parse_dates=['buyDate','sellDate'])
df['length'] = pd.to_datetime(df['sellDate']).subtract(pd.to_datetime(df['buyDate']))
print('length')
print("win length")