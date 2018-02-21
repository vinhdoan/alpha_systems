import requests
from lxml import html
import pandas as pd


def fetch_table(code, page):
    url = 'http://s.cafef.vn/Lich-su-giao-dich-' + code + '-3.chn'
    headers = {'Host': 's.cafef.vn',
               'Connection': 'keep-alive',
               'Cache-Control': 'no-cache',
               'Origin': 'http://s.cafef.vn',
               'X-MicrosoftAjax': 'Delta=true',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Accept': '*/*',
               'Referer': url,
               'Accept-Language': 'en-US,en;q=0.9'}
    payload = 'ctl00%24ContentPlaceHolder1%24scriptmanager=ctl00%24ContentPlaceHolder1%24ctl03%24panelAjax%7Cctl00%24ContentPlaceHolder1%24ctl03%24pager1&ctl00%24ContentPlaceHolder1%24ctl03%24txtKeyword=' + code + '&ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate1%24txtDatePicker=&ctl00%24ContentPlaceHolder1%24ctl03%24dpkTradeDate2%24txtDatePicker=&ctl00%24UcFooter2%24hdIP=&__EVENTTARGET=ctl00%24ContentPlaceHolder1%24ctl03%24pager1&__EVENTARGUMENT=' + str(page) + '&__VIEWSTATE=%2FwEPDwUKMTU2NzY0ODUyMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFKGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkY3RsMDMkYnRTZWFyY2jJnyPYjjwDsOatyCQBZar0ZSQygQ%3D%3D&__VIEWSTATEGENERATOR=2E2252AF&__ASYNCPOST=true&'

    r = requests.post(url, headers=headers, data=payload)
    h = html.fromstring(r.text.split('|')[11].strip())
    return h.findall('table/tr')


titles = ['Date',
          'KL giao dich rong',
          'Gia tri giao dich rong',
          'Thay doi',
          'Mua/Khoi luong',
          'Mua/Gia tri',
          'Ban/Khoi luong',
          'Ban/Gia tri',
          'Room con lai',
          'Dang so huu',]
mainDF = pd.DataFrame(columns=titles)
page = 1
# df = pd.read_csv('latestData.csv')
# results = pd.DataFrame(columns=['Stock', 'Quarterly', 'Yearly'])
# stockList = df.Stock
# stockList = stockList.drop_duplicates()
# stockList = stockList.reset_index(drop=True)
vn30 = ['CTD','KBC','BID','NT2','MBB','BVH','VCB','MSN','CII','BMP','DHG','DPM','FPT','GMD','HPG','HSG','KDC','MWG','PVD','REE','SBT','SSI','STB','VIC','CTG','GAS','VNM','ROS','SAB','NVL']
for i in range(len(vn30)):
    print(vn30[i])
    page = 1
    while True:
        rows = fetch_table(vn30[i], page)
        if len(rows) <= 2:
            break
        print('\rCurrent page:', page, end='')
        page += 1
        df = pd.DataFrame(columns=titles)
        for index, row in enumerate(rows[2:]):
            cells = row.findall('td')
            rowDict = {}
            for k, v in zip(titles, cells):
                rowDict[k] = v.text.strip('\xa0')
            df.loc[index] = rowDict
        df['Stock'] = vn30[i]
        mainDF = pd.concat([mainDF, df], ignore_index=True)


mainDF.to_csv('cafef_tx_history.csv',index=False)
