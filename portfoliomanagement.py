
import requests
import math
import time
from datetime import timedelta,date,datetime
import pandas as pd
import numpy as np
import json
import requests
from operator import itemgetter

webhook_url = 'https://hooks.slack.com/services/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'
df = pd.read_csv('checkPoint/last-portfolio.csv')
alertIndex = []
df = df.loc[df.Closed==0]
df = df.reset_index(drop=True)
stockList = df.Stock
stockList = stockList.drop_duplicates()
buyStocks = 'mua duoc '
# columns = Stock	Volume	BuyPrice	CurrentPrice	TakeProfit	StopLoss	Upnl	Pnl	Closed
now = datetime.now()
#market close @ 2:45pm, give some delay time
todayClose = now.replace(hour=23,minute=48,second=0,microsecond=0)
while datetime.now()<todayClose:
    for i in range(len(df)):
        if df.ix[i]['Stock'] not in alertIndex:
            url = 'https://price-hcm04.vndirect.com.vn/priceservice/derivative/transactions/q=symbol:' +df.ix[i]['Stock']
            result = requests.get(url)
            if result.status_code == 200:
                jsonData = result.json()
                symbol = jsonData['symbol']
                if len(symbol) == 3:
                    data = jsonData['data']
                    if (len(data) > 0):
                        data = sorted(data, key=itemgetter('time'))
                        last = (data[len(data) - 1]['last'])
                        highest = (data[len(data) - 1]['highest'])
                        lowest = (data[len(data) - 1]['lowest'])
                        if last >= df.ix[i]['TakeProfit']:
                            slackdata = {'text': "@vinhdoan take profit: " + symbol + " - " + '%.2f' % last}
                            response = requests.post(
                                webhook_url, data=json.dumps(slackdata),
                                headers={'Content-Type': 'application/json'}
                            )
                            alertIndex.append(symbol)
                        if lowest <= df.ix[i]['StopLoss']:
                            print(lowest)
                            slackdata = {'text': "@vinhdoan CUT LOSS NOW!!: " + symbol + " - " + '%.2f' % last}
                            response = requests.post(webhook_url, data=json.dumps(slackdata),
                                headers={'Content-Type': 'application/json'})
                            alertIndex.append(symbol)
                            # += symbol +'-'
    print(datetime.now().time())
    time.sleep(2)