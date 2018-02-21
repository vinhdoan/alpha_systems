import numpy as np
import pandas as pd
from scipy.stats.stats import pearsonr

'''
SAB 0.88242401736493437
GAS 0.94934150482924629'
VNM 0.91509356357885407'
BID 0.94132876737707216
MBB 0.91135672905923637
MSN 0.88401527039945915
FPT 0.96907035655576701
MWG 0.89411049235754714
CTG 0.92768392170131397
VIC 0.98244702827902419
VCB 0.97255655215841208,
'''

def correlationTest():
    df1 = pd.read_csv('futures/VN30.csv', parse_dates=['Date'])
    a = np.asarray(df1.Close)
    # df2 = pd.read_csv('data/VN30F1M.csv')
    # b = np.asarray(df2.Close)
    vn30 = ['CTD','KBC','BID','NT2','MBB','BVH','VCB','MSN','CII','BMP','DHG','DPM','FPT','GMD','HPG','HSG','KDC','MWG','PVD','REE','SBT','SSI','STB','VIC','CTG','GAS','VNM','ROS','SAB','NVL']
    for i in range(len(vn30)):
        checkStock = pd.read_csv('data/'+vn30[i]+'.csv', index_col=0, parse_dates=['Date'])
        test = checkStock.ix[len(checkStock) - 90:len(checkStock) - 1]
        c = np.asarray(test.Close)
        print(vn30[i],pearsonr(b,c))

def getWeight(stock):
    # if stock=='SAB':
    #     return 0.882424
    if stock=='GAS':
        return 0.94934150482924629
    # if stock=='VNM':
    #     return 0.91509356357885407
    if stock=='BID':
        return 0.94132876737707216
    # if stock=='MBB':
    #     return 0.91135672905923637
    # if stock=='MSN':
    #     return 0.88401527039945915
    if stock=='FPT':
        return 0.96907035655576701
    # if stock=='MWG':
    #     return 0.89411049235754714
    # if stock=='CTG':
    #     return 0.92768392170131397
    if stock=='VIC':
        return 0.98244702827902419
    # if stock=='SAB':
    #     return 0.882424
    if stock=='VCB':
        return 0.97255655215841208
    else:
        return 0.00


def tryCorrelationTest():
    vn30 = ['CTD', 'KBC', 'BID', 'NT2', 'MBB', 'BVH', 'VCB', 'MSN', 'CII', 'BMP', 'DHG', 'DPM', 'FPT', 'GMD', 'HPG',
            'HSG', 'KDC', 'MWG', 'PVD', 'REE', 'SBT', 'SSI', 'STB', 'VIC', 'CTG', 'GAS', 'VNM', 'ROS', 'SAB', 'NVL']
    df1 = pd.read_csv('futures/VN30.csv', parse_dates=['Date'])
    a = np.asarray(df1.Close)
    # df2 = pd.read_csv('data/VN30F1M.csv')
    # b = np.asarray(df2.Close)
    mainSet = pd.DataFrame(columns=['Date','Open','High','Low','Close','Volume','change'])
    totalWeight = 0
    for i in range(len(vn30)):
        w = (float)(getWeight(vn30[i]))
        if w > 0.8:
            totalWeight += w
            checkStock = pd.read_csv('data/'+vn30[i]+'.csv', index_col=0, parse_dates=['Date'])
            test = checkStock.ix[len(checkStock) - 90:len(checkStock)]
            test['change'] = w * (test['Close'] - test['Close'].shift(-1))
            test = test.ix[0:len(test)-1]
            if len(mainSet)==0:
                mainSet = pd.concat([mainSet,test])
            else:
                mainSet['change'] = mainSet['change'] + test['change']
    mainSet['change'] = mainSet['change']/totalWeight
    # print(vn30[i],pearsonr(b,c))
    mainSet['change'].to_csv('testFuture1.csv')

if __name__ == '__main__':
    correlationTest()