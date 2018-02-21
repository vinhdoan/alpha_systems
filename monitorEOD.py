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

webhook_url = 'https://hooks.slack.com/services/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'
df = pd.read_csv('latestData.csv')
df['Alert'] = 0
alertIndex = []
stockList = df.Stock
stockList = stockList.drop_duplicates()
buyStock = 'DTG thong bao: danh sach khuyen nghi: '
now = datetime.now()
#market close @ 2:45pm, give some delay time
todayClose = now.replace(hour=14,minute=48,second=0,microsecond=0)

for i in range(len(df)):
    if df.ix[i]['Stock'] not in alertIndex:
        url = 'https://price-hcm04.vndirect.com.vn/priceservice/derivative/transactions/q=symbol:'+ df.ix[i]['Stock']
        result = requests.get(url)
        if result.status_code==200:
            jsonData = result.json()
            symbol = jsonData['symbol']
            if len(symbol)==3:
                data = jsonData['data']
                if(len(data)>0):
                    last = (data[len(data)-1]['last'])
                    highest = (data[len(data) - 1]['highest'])
                    vol = (data[len(data) - 1]['accumulatedVol'])
                    if last >= df.ix[i]['52weeksHigh'] and highest >= df.ix[i]['High']*1.03 and vol>3000:
                        slackdata = {'text': "mua được:" + symbol+ " - " + '%.2f' % last}
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
