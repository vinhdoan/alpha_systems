
fileList = glob.glob('rawdata/*.csv')
yearHighList = pd.DataFrame(columns=['Stock','Date','Open','High','Low','Close','Volume','52weeksHigh','averageVol'])
for fileName in fileList:
    df = pd.read_csv(fileName)
    df.columns = ['Stock','Date','Open','High','Low','Close','Volume']
    stockList = df.ix[:,0]
    stockList = stockList.drop_duplicates()
    for stock in stockList:
        checkStock = df[df['Stock'].isin([stock])]
        checkStock = checkStock.reset_index(drop=True)
        checkStock['Date'] = pd.to_datetime(checkStock['Date'].astype(str), format='%Y%m%d')
        checkStock = checkStock.sort_values('Date')
        checkStock = checkStock.reset_index(drop=True)
        checkStock["52weeksHigh"] = checkStock.High.rolling(window=252, min_periods=1, center=False).max()
        checkStock["averageVol"] = checkStock.Volume.rolling(window=10, min_periods=1, center=False).mean()
        #yearHighList.loc[i] = [stock, checkStock.ix[len(checkStock-1)]['Date'], checkStock.ix[len(checkStock-1)]['Open'], checkStock.ix[len(checkStock-1)]['High'], checkStock.ix[len(checkStock-1)]['Low'], checkStock.ix[len(checkStock-1)]['Close'], checkStock.ix[len(checkStock-1)]['Volume'], checkStock.ix[len(checkStock-1)]['52weeksHigh'], checkStock.ix[len(checkStock-1)]['averageVol']]
        if checkStock.ix[len(checkStock)-1]['averageVol'] > 20000:
            yearHighList = yearHighList.append(checkStock.ix[len(checkStock)-1])
        temp = checkStock[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        temp.to_csv('data/'+stock+'.csv',index=False)


yearHighList.to_csv('latestData.csv',index=False)