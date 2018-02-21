'''
vcb, fpt, vic
'''

import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr

if __name__ == '__main__':
    df = pd.read_csv('data/VN30F1M.csv')
    test1 = pd.read_csv('data/VCB.csv')
    test2 = pd.read_csv('data/VIC.csv')
    test3 = pd.read_csv('data/FPT.csv')
    df['ret'] = df['Close'] / df['Open'].shift(1) - 1
    test1['ret'] = test1['Close']/test1['Close'].shift(1) - 1
    test2['ret'] = test2['Close'] / test2['Close'].shift(1) - 1
    test3['ret'] = test3['Close'] / test3['Close'].shift(1) - 1
    t1 = test1.ix[len(test1) - 91:len(test1) - 3]

    t2 = test2.ix[len(test2) - 91:len(test2) - 3]
    t3 = test3.ix[len(test3) - 91:len(test3) - 3]
    t1 = t1.reset_index(drop=True)
    t2 = t2.reset_index(drop=True)
    t3 = t3.reset_index(drop=True)
    #print(t1)

    # print(t1)
    won = 0
    loss = 0
    c1=0
    c2=0
    sumWon =0
    sumLoss = 0
    for i in range(len(df)):
        if (t1.ix[i]['ret']<=-0.008 and t2.ix[i]['ret']<=-0.008) or (t2.ix[i]['ret']<=-0.008 and t3.ix[i]['ret']<=-0.008) or (t1.ix[i]['ret']<=-0.008 and t3.ix[i]['ret']<=-0.008):
            if df.ix[i]['ret'] < 0:
                won+=1
                sumWon += df.ix[i]['ret']
                c1+=1
            else:
                loss +=1
                sumLoss += df.ix[i]['ret']
                c2+=1

        if (t1.ix[i]['ret'] >= 0.008 and t2.ix[i]['ret'] >= 0.008) or (
                t2.ix[i]['ret'] >= 0.008 and t3.ix[i]['ret'] >= 0.008) or (
                t1.ix[i]['ret'] >= 0.008 and t3.ix[i]['ret'] >= 0.008):
            if df.ix[i]['ret'] > 0:
                won += 1
                sumWon += -df.ix[i]['ret']
                c1 += 1
            else:
                loss += 1
                sumLoss += -df.ix[i]['ret']
                c2 += 1
            #count+=1
    print(won,loss)
    print(sumWon/c1,sumLoss/c2)
    print((sumWon/c1)/(sumLoss/c2))