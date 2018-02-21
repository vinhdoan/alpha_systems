import numpy as np
import pandas as pd


if __name__ == '__main__':
    df = pd.read_csv('testresults/52wksbreakout-buySellClose-20percent.csv')
    # df['consecutiveWon'] = (df.status.diff(1) != 0).astype('int').cumsum()
    max = 0
    temp = 0
    for i in range(len(df)):
        if df.ix[i].status == 'loss':
            temp += 1
            if temp > max:
                max = temp
                # if temp == 12:
                #     print(df.ix[i]['stock'] + str(df.ix[i]['buyDate']))
        else:
            temp = 0
    print(max)
