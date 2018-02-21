
import numpy as np
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('data/VN30F1M.csv')
    test1 = pd.read_csv('data/VCB.csv')
    # test2 = pd.read_csv('data/VIC.csv')
    # test3 = pd.read_csv('data/FPT.csv')
    # df['ret'] = df['Close'] / df['Open'] - 1

    test1['ret'] = test1['Close'] / test1['Close'].shift(1) - 1
    # test2['ret'] = test2['Close'] / test2['Close'].shift(-1) - 1
    # test3['ret'] = test3['Close'] / test3['Close'].shift(-1) - 1
    print(test1)
