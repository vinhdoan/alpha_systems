import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup as bs


#
#
# url = 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=ttb&Type=1&PageIndex=0'
# results = requests.get(url)
# content = results.content
# soup = bs(content,'lxml')
# rows = soup.find_all('td')
# print(rows[6].string)


# PBIT: profit before interest tax and taxation
'''
PBIT = 15. Tong loi nhuan ke toan truoc thue + chi phi lai vay
capital employed = total assets less currant liabilities = Tổng tài sản	- tong no ngan han
profit margin = gross profit / sales

asset turnover = sales / total assets less current liabilities

A/cs receivable collection period:
trade receivables: phải thu khách hàng
net sales = doanh thu ban hang va cung cap dich vu - cac khoan giam tru doanh thu

turnover = cost of sales (COGS) / average inventory (this year inv + last year inv)/2

A/cs payable payment period:
Trade account payable / purchases x 365

gearing ratio = prior charge capital / total capital

'''

'''
so sanh loi nhuan tang quy gan nhat so voi cung ki nam truoc
so sanh loi nhuan tang binh quan 4 nam gan nhat
'''
def getFundamentalInfo(stock):
    # ('doanh thu , loi nhuan quý cuối và cùng kỳ năm ngoái')
    url1 = 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=' +stock + '&Type=1&PageIndex=4'
    a = []
    results = requests.get(url1)
    content = results.content
    soup = bs(content, 'lxml')
    rows = soup.find_all('td')
    # for i in range(len(rows)):
    #     print(i, rows[i].string)
    # print(heads[4].string,rows[6].string)
    if len(rows)>4:
        for j in range(len(rows)):
            if rows[j].string == "Tổng lợi nhuận trước thuế":
                if (rows[j+4].string != u'\xa0'):
                    quy3 = rows[j+4].string.replace(",","")
                    url2 = 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=' + stock +'&Type=1&PageIndex=0'
                    results = requests.get(url2)
                    content = results.content
                    soup = bs(content, 'lxml')
                    rows = soup.find_all('td')
                    for k in range(len(rows)):
                        if rows[k].string=="Tổng lợi nhuận trước thuế":
                            if rows[k+4].string!= u'\xa0':
                                quy31 = rows[k+4].string.replace(",", "")
                                quaterEarnings = ((float)(quy31) / (float)(quy3) - 1) * 100
                                a.append(quaterEarnings)

    # ('doanh thu , loi nhuan 4 nam gan nhat')
    url3 = 'http://s.cafef.vn/Ajax/HoSoCongTy.aspx?symbol=' + stock +'&Type=2&PageIndex=0'
    results = requests.get(url3)
    content = results.content
    soup = bs(content, 'lxml')
    rows = soup.find_all('td')
    # the empty result is u'\xa0'
    if len(rows)>4:
        for n in range(len(rows)):
            if rows[n].string =="Tổng lợi nhuận trước thuế":
                if rows[n+1].string!=u'\xa0' and rows[n+2].string!=u'\xa0' and rows[n+3].string!=u'\xa0' and rows[n+4].string!=u'\xa0':
                    y1 = (float)(rows[n+1].string.replace(",",""))
                    y2 = (float)(rows[n+2].string.replace(",", ""))
                    y3 = (float)(rows[n+3].string.replace(",", ""))
                    y4 = (float)(rows[n+4].string.replace(",", ""))
                    yearlyEarning = (((y2/y1) + (y3/y2) + (y4/y3)) / 3 - 1)*100
                    a.append(yearlyEarning)
    j = 0
    k= 0
    n = 0
    return a

if __name__ == '__main__':
    df = pd.read_csv('latestData.csv')
    results = pd.DataFrame(columns=['Stock','Quarterly','Yearly'])
    stockList = df.Stock
    stockList = stockList.drop_duplicates()
    stockList = stockList.reset_index(drop=True)
    # bank = ['ACB', 'BID', 'CTG','EIB','KLB','LPB','MBB','NVB','SHB','STB','VCB','VIB','VPB']
    ignore = ['L14', 'NGC', 'SVN', 'PIC']
    for i in range(len(stockList)):
        if stockList[i] not in ignore:
            print(stockList[i])
            try:
                b = getFundamentalInfo(stockList[i])
                if len(b)==2:
                    temp = pd.DataFrame([[stockList[i],b[0],b[1]]], columns=['Stock','Quarterly','Yearly'])
                    results = pd.concat([results,temp])
            except Exception as exception:
                print(exception)
    results.to_csv('fundamentals1.csv')
