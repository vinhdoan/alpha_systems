#!/usr/bin/env python3

# note: @ ATO and ATC: KL_KhopLenh = null



import requests
import math
import time
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
from twilio.rest import Client
import json
import requests
from operator import itemgetter
import fundamentals as fa
from decimal import Decimal

webhook_url = 'https://hooks.slack.com/services/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'
df = pd.read_csv('latestData.csv')
df['Alert'] = 0
alertIndex = []
stockList = df.Stock
stockList = stockList.drop_duplicates()
now = datetime.now()
#market close @ 2:45pm, give some delay time
todayClose = now.replace(hour=15,minute=48,second=0,microsecond=0)
# tradable value
kis = 466000
fpt = 53000


while datetime.now()<todayClose:
    for i in range(len(stockList)):
        if df.ix[i]['Stock'] not in alertIndex:
            url = 'https://price-hcm04.vndirect.com.vn/priceservice/derivative/transactions/q=symbol:'+ df.ix[i]['Stock']
            result = requests.get(url)
            if result.status_code==200:
                jsonData = result.json()
                symbol = jsonData['symbol']
                if len(symbol)==3:
                    data = jsonData['data']
                    if(len(data)>0):
                        data = sorted(data, key=itemgetter('time'))
                        open = data[0]['last']
                        last = (data[len(data)-1]['last'])
                        lowest = (data[len(data) - 1]['lowest'])
                        vol = (data[len(data) - 1]['accumulatedVol'])
                        if last >= df.ix[i]['3monthlow'] and lowest <= df.ix[i]['3monthlow']: #open >= df.ix[i]['High'] and
                            mgK = "no"
                            mgF = "no"
                            financialData = fa.getFundamentalInfo(symbol)
                            # financialData = []
                            info = ""
                            if len(financialData)==2:
                                print(symbol)
                                info = '\n' + 'tăng trưởng quý 3 so với cùng kì: '+ "{0:.2f}".format(financialData[0]) + " %" + '\n' + 'tăng trưởng bình quân 4 năm: '+ "{0:.2f}".format(financialData[1]) + " %"
                            slackdata = {'text': "mean-reverse:" + symbol+ " - " + '%.2f' % last + ' tối đa ' + str(int(df.ix[i]['averageVol']/20)) + " cổ phiếu" + info+ '\n'+'---------------'}
                            response = requests.post(
                                        webhook_url, data=json.dumps(slackdata),
                                        headers={'Content-Type': 'application/json'}
                                    )
                            if response.status_code != 200:
                                raise ValueError(
                                    'Request to slack returned an error %s, the response is:\n%s'
                                    % (response.status_code, response.text)
                                )
                            else:
                                alertIndex.append(df.ix[i]['Stock'])
                                buyStock = buyStock + symbol +' va '
    #if buyStock!='DTG thong bao: danh sach khuyen nghi: ':
        #sms = 'http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=0868291125&Content='+buyStock+'&ApiKey=1379D32BB315F672631578B6C9C724&SecretKey=EC064FDB3E4D27F06F2B12FDDD0052&SmsType=8'
        #send = requests.get(sms)
        # sms = 'http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get?Phone=0977092137&Content=' + buyStock + '&ApiKey=1379D32BB315F672631578B6C9C724&SecretKey=EC064FDB3E4D27F06F2B12FDDD0052&SmsType=8'
        # send = requests.get(sms)
    buyStock = 'DTG thong bao: danh sach khuyen nghi: '
    print(datetime.now().time())
    time.sleep(10)