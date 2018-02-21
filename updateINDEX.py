from datetime import date, timedelta
import wget
import os
import zipfile
import numpy as np
import pandas as pd
import glob
#clean the folder
# dirname = 'rawdata/'
# for file in os.listdir(dirname):
#     filepath = os.path.join(dirname,file)
#     os.remove(filepath)
# #get the fileName
# today = date.today() - timedelta(0)
# todayString = today.strftime('%d%m%Y')
# todayString2 = today.strftime('%Y%m%d')
# url = 'http://images1.cafef.vn/data/' + todayString2 + '/CafeF.SolieuGD.Upto' + todayString + '.zip'
# #download and unzip
# zipFile = wget.download(url)
# zip_ref = zipfile.ZipFile(zipFile,'r')
# zip_ref.extractall('rawdata/')
# zip_ref.close()
#
#
# fileList = glob.glob('rawdata/*.csv')
# yearHighList = pd.DataFrame(columns=['Stock','Date','Open','High','Low','Close','Volume','52weeksHigh','averageVol'])
# for fileName in fileList:
df = pd.read_csv('index.csv')
df.columns = ['Stock','Date','Open','High','Low','Close','Volume']
stockList = df.ix[:,0]
stockList = stockList.drop_duplicates()
for stock in stockList:
    # if len(stock)==3:
    checkStock = df[df['Stock'].isin([stock])]
    checkStock = checkStock.reset_index(drop=True)
    checkStock['Date'] = pd.to_datetime(checkStock['Date'].astype(str), format='%Y%m%d')
    checkStock = checkStock.sort_values('Date')
    checkStock = checkStock.reset_index(drop=True)
    checkStock["52weeksHigh"] = checkStock.High.rolling(window=252, min_periods=1, center=False).max()
    checkStock["averageVol"] = checkStock.Volume.rolling(window=10, min_periods=1, center=False).mean()
    #yearHighList.loc[i] = [stock, checkStock.ix[len(checkStock-1)]['Date'], checkStock.ix[len(checkStock-1)]['Open'], checkStock.ix[len(checkStock-1)]['High'], checkStock.ix[len(checkStock-1)]['Low'], checkStock.ix[len(checkStock-1)]['Close'], checkStock.ix[len(checkStock-1)]['Volume'], checkStock.ix[len(checkStock-1)]['52weeksHigh'], checkStock.ix[len(checkStock-1)]['averageVol']]
    # if checkStock.ix[len(checkStock)-1]['averageVol'] > 20000 and len(checkStock)>252:
    #     yearHighList = yearHighList.append(checkStock.ix[len(checkStock)-1])
    temp = checkStock[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    temp.to_csv('data/'+stock+'.csv',index=False)
# yearHighList = yearHighList.sort_values('Stock')
# yearHighList = yearHighList.reset_index(drop=True)
# yearHighList.to_csv('latestData.csv',index=False)