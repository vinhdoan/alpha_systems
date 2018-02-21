'''
only trade those with daily transaction value > 2.5 account valua
only trade with 1/8
'''

from datetime import date, timedelta
import wget
import os
import zipfile
import numpy as np
import pandas as pd
import glob



if __name__ == '__main__':
    '''
    - Example: Specify both stock and host
        get_stocks(host="https://price-hcm07.vndirect.com.vn",
                   codeList=['BVH', 'CII'])
    - 'host' can be omitted -> a bit slow because the program will ping every
                               hosts to get the nearest one
    - 'codeList' can be omitted -> default all stocks will be fetched
    - Order in 'codeList' is arbitrary. Stock will be sorted in dataframe.
    '''

    df = pd.read_csv('latestData.csv')
    a = df.Stock.tolist()
    print(get_stocks(
        host="https://price-hcm07.vndirect.com.vn",
        codeList=a
    ))