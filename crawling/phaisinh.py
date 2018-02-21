'''
get vn30 for every 10 seconds
get vn30f1m for every 10 seconds
get vn30f2m for every 10 seconds
stored all into time series
stored to .csv for analyzing
'''

import requests
from datetime import date, datetime
import time
import math
import pandas as pd


def get_timestamp():
    return str(math.floor(time.time() * 1000))


def choose_pricehost():
    # url = "https://banggia-hcm.vndirect.com.vn/pricehosts/"
    # result = requests.get(url)
    # priceHosts = result.json()['hosts']
    # appendage = "/?ping=jQuery32104866340602383221_" + get_timestamp() + "&_=" + get_timestamp()
    # minElapsedTime = timedelta.max
    # chosenHost = ""
    # for host in priceHosts:
    #     url = host + appendage
    #     result = requests.get(url)
    #     if result.ok:
    #         elapsedTime = result.elapsed
    #         if elapsedTime < minElapsedTime:
    #             minElapsedTime = elapsedTime
    #             chosenHost = host
    return "https://price-hcm04.vndirect.com.vn"


def get_derivatives(host=None):
    if not host:
        host = choose_pricehost()
    # print("Host has been chosen:", host)
    appendage = "/priceservice/derivative/snapshot/q=floorCode:DER01"
    url = host + appendage
    result = requests.get(url)
    return result.json()['DER01']


def parse_derivatives(ders):
    '''
    Reference: https://trade-hcm.vndirect.com.vn/chung-khoan/phai-sinh
    For each derivative:
    - Ma HD           : 14
    - Ngay DH         : 24
    - TC              : 3, 40
    - Tran            : 12
    - San             : 22
    - Tong KL         : 1, 50
    - KL mo (OI)      : 37
    - Du mua / Gia 3  : 7
    - Du mua / KL 3   : 10
    - Du mua / Gia 2  : 6
    - Du mua / KL 2   : 9
    - Du mua / Gia 1  : 5
    - Du mua / KL 1   : 8
    - Khop lenh / Gia : 13, 16, 27
    - Khop lenh / KL  : 28
    - Khop lenh / +-  : ?
    - Du ban / Gia 1  : 31
    - Du ban / KL 1   : 34
    - Du ban / Gia 2  : 32
    - Du ban / KL 2   : 35
    - Du ban / Gia 3  : 33
    - Du ban / KL 3   : 36
    - Gia / Mo cua    : 38
    - Gia / Cao       : 23
    - Gia / Thap      : 26
    - DTNN / Mua      : ?
    - DTNN / Ban      : ?
    '''
    derList = []
    for der in ders:
        derAttrs = der.split('|')
        maHD = derAttrs[14]
        tongKL = int(float(derAttrs[1]) * 10)
        giaKhopLenh = float(derAttrs[27]) * 1000
        klKhopLenh = int(float(derAttrs[28]) * 10)
        derList.append([maHD, tongKL, giaKhopLenh, klKhopLenh])
    derList.sort()
    ind = 1
    df = pd.DataFrame(columns=["ID","Instrument", "Volume", "Price", "TransactedVolume"])
    for der in derList:
        der.insert(0, ind)
        df.loc[len(df)] = der
        ind += 1
    vn30 = getvn30()
    df = pd.concat([df,pd.DataFrame([[5,"VN30",0,vn30,0]],columns=["ID", "Instrument", "Volume", "Price", "TransactedVolume"])])
    df["datetime"] = datetime.now()
    return df  # pandas DataFrame

def getvn30():
    url = 'https://price-hcm04.vndirect.com.vn/priceservice/market/snapshot/q=codes:11'
    result = requests.get(url)
    response = result.json()
    data = response['11']['data']['marketIndex']
    return data

if __name__ == '__main__':
    now = datetime.now()
    todayClose = now.replace(hour=14, minute=45, second=0, microsecond=0)
    result = []
    final = pd.DataFrame(columns=["ID", "Instrument", "Volume", "Price", "TransactedVolume","datetime"])
    while datetime.now() < todayClose:
        # result.append(getvn30())
        print(datetime.now().time())
        # print(result)
        ders = get_derivatives("https://price-hcm04.vndirect.com.vn")
        a = parse_derivatives(ders)
        final = pd.concat([final,a])
        time.sleep(2)
    final.to_csv('testphaisinh.'+ datetime.now() + '.csv')