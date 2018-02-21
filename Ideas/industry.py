'''
list industry co phieu 68
^bds: bat dong san
^caosu: cao su
^ck: chung khoan
^congnghe: cong nghe vien thong
^dichvu: dich vu du lich
^dvci: dich vu cong ich
^duocpham: duoc
^giaoduc: giao duc
^hk: hang khong
^khoangsan: khoang san
^nangluong: nang luong / dien khi
^nganhang: ngan hang - bao hiem
^thep: thep
^daukhi: dau khi
^nhua: nhua bao bi
^phanbon: phan bon
^sxkd: san xuat kinh doanh
^thucpham:thuc pham, VNM, SAB
^thuongmai: thuong mai PNJ, MWG
^thuysan: thuy san
^vantai: van tai / cang / taxi
^vlxd: vat lieu xay dung
^xaydung: xay dung
^dtpt: dau tu phat trien
^dtxd: dau tu xay dung: CII



'''

import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup as bs
new_table = pd.DataFrame(columns=['Industry','Stock','+/-',	'EPS',	'PE',	'ROA',	'ROE',	'Giá SS',	'P/B',	'Beta'	,'totalVolume'	,'NN'	,'von'])
industries = ['bds','caosu','ck','congnghe','dichvu','dvci','duocpham','giaoduc','hk','khoangsan','nangluong','nganhang','thep','daukhi','nhua','phanbon','sxkd','thucpham','thuongmai','thuysan','vantai','vlxd','xaydung','dtpt','dtxd']
for industry in industries:
    url = 'http://www.cophieu68.vn/categorylist_detail.php?category=^'+industry
    result = requests.get(url)

    html_string = result.content

    soup = bs(html_string, 'lxml')  # Parse the HTML as a string

    # table = soup.find_all('table')[0]  # Grab the first table


    items = soup.find_all('td')
    if len(items)>0:
        noOfStocks = (len(items)-2-13)/13
        i = 1
        while i<noOfStocks:
            stt = items[2+i*13].get_text()
            stock = items[2+i*13+1].get_text()
            pnl = items[2 + i * 13 + 2].get_text()
            eps= items[2 + i * 13 + 3].get_text()
            pe= items[2 + i * 13 + 4].get_text()
            roa= items[2 + i * 13 + 5].get_text()
            roe= items[2 + i * 13 + 6].get_text()
            bookValue = items[2 + i * 13 + 7].get_text()
            pb = items[2 + i * 13 + 8].get_text()
            beta = items[2 + i * 13 + 9].get_text()
            tongKL = items[2 + i * 13 + 10].get_text()
            nn = items[2 + i * 13 + 11].get_text()
            von = items[2 + i * 13 + 12].get_text()
            newRow = pd.DataFrame([[industry,stock,pnl,eps,pe,roa,roe,bookValue,pb,beta,tongKL,nn,von]],columns=['Industry','Stock','+/-',	'EPS',	'PE',	'ROA',	'ROE',	'Giá SS',	'P/B',	'Beta'	,'totalVolume'	,'NN' 	,'von'])
            new_table = pd.concat([new_table,newRow])
            i +=1





# row_marker = 0
# rows = table.find_all('tr')
# print(len(rows))
# for row in rows:
#     column_marker = 0
#     columns = row.find_all('td')
#     print(len(columns))
#     for column in columns:
#         new_table.iat[row_marker, column_marker] = column.get_text()
#         column_marker += 1

# print(new_table)
new_table.to_csv('fundamental/generalInfo.csv')