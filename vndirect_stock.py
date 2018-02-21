#!/usr/bin/env python3

import requests
import math
import time
from datetime import timedelta
import pandas as pd
import time
from datetime import datetime, date, timedelta

def get_timestamp():
    return str(math.floor(time.time() * 1000))


def choose_pricehost():
    url = "https://banggia-hcm.vndirect.com.vn/pricehosts/"
    result = requests.get(url)
    priceHosts = result.json()['hosts']
    appendage = "/?ping=jQuery32104866340602383221_" + get_timestamp() + "&_=" + get_timestamp()
    minElapsedTime = timedelta.max
    chosenHost = ""
    for host in priceHosts:
        url = host + appendage
        result = requests.get(url)
        if result.ok:
            elapsedTime = result.elapsed
            if elapsedTime < minElapsedTime:
                minElapsedTime = elapsedTime
                chosenHost = host
    return chosenHost


def get_stocks(host=None, codeList=[]):
    if not host:
        host = choose_pricehost()
    print("Host has been chosen:", host)

    jsonpPrefix = "jQuery21407643729406387143_"
    jsonpName = jsonpPrefix + get_timestamp()
    queryParams = "?jsonp=" + jsonpName + "&_=" + get_timestamp()
    path = "/priceservice/secinfo/snapshot/"
    if not codeList:  # list is empty -> get all stock codes
        query = "q=floorCode:10"
    else:
        query = "q=codes:" + ','.join(codeList)
    appendage = path + query + queryParams
    url = host + appendage
    print("Url:", url)
    result = requests.get(url)
    if result.ok:
        exec(jsonpName + " = create_handler()")
        return eval(result.content)
    else:
        raise Exception('Cannot get stocks')


def create_handler():
    def handler(returnValue):
        '''
        Reference: https://banggia-hcm.vndirect.com.vn/chung-khoan/#khop-lenh/hose
        For each stock:
        - Ma CK              : 3
        - TC                 : 8
        - Tran               : 15
        - San                : 16
        - Tong KL            : 36
        - Gia 3 / Mua        : 27
        - KL 3 / Mua         : 28
        - Gia 2 / Mua        : 25
        - KL 2 / Mua         : 26
        - Gia 1 / Mua        : 23
        - KL 1 / Mua         : 24
        - Gia / Khop lenh    : 19
        - KL / Khop lenh     : 20
        - +/- / Khop lenh    : ?
        - Gia 1 / Ban        : 29
        - KL 1 / Ban         : 30
        - Gia 2 / Ban        : 31
        - KL 2 / Ban         : 32
        - Gia 3 / Ban        : 33
        - KL 3 / Ban         : 34
        - Cao / Gia          : 13
        - TB / Gia           : ?
        - Thap / Gia         : 14
        - Mua / Du           : ?
        - Ban / Du           : ?
        - Mua / DTNN         : 37
        - Ban / DTNN         : 38
        - <time>             : 2
        - <unknown timestamp>: 1
        '''
        if type(returnValue) is dict:
            returnList = returnValue["10"]
        else:
            returnList = returnValue

        # Generate and sort list of stocks
        stockList = []
        for stock in returnList:
            stockAttrs = stock.split('|')

            # Ma chung khoan
            maCK = stockAttrs[3]

            # Gia & khoi luong khop lenh
            giaKhopLenh = float(stockAttrs[19]) if stockAttrs[19] else 0.0
            klKhopLenh = int(stockAttrs[20]) if stockAttrs[20] else 0

            stockList.append([maCK, giaKhopLenh, klKhopLenh])
        stockList.sort()

        # Convert list to pandas dataframe
        ind = 1
        df = pd.DataFrame(columns=["ID", "MaCK", "Gia_KhopLenh", "KL_KhopLenh"])
        for stock in stockList:
            stock.insert(0, ind)
            df.loc[len(df)] = stock
            ind += 1
        return df  # pandas DataFrame
    return handler

def getVN30():
    return ['CTD','KBC','BID','NT2','MBB','BVH','VCB','MSN','CII','BMP','DHG','DPM','FPT','GMD','HPG','HSG','KDC','MWG','PVD','REE','SBT','SSI','STB','VIC','CTG','GAS','VNM','ROS','SAB','NVL']

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


    a = ['VN30F1802']


    print(get_stocks(
        host="https://price-hcm07.vndirect.com.vn",
        codeList=a
    ))
