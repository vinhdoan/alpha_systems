import numpy as np
import pandas as pd
import requests

from bs4 import BeautifulSoup as bs

def clean_text(row):
    # return the list of decoded cell in the Series instead
    return [r.encode('ascii', 'ignore') for r in row]



source = pd.read_csv('latestData.csv')
df = pd.DataFrame(columns=['stock','STT','indicator','2017','2016','2015','2014','2013'])
for i in range(len(source)):
    url = 'http://www.cophieu68.vn/statistic_index.php?currentPage=1&id=' + source.ix[i]['Stock']
    result = requests.get(url)
    html_string = result.content
    soup = bs(html_string, 'lxml')  # Parse the HTML as a string
    items = soup.find_all('table')
    # print(len(items))
    # print(items[1])
    # print(items[3])
    if len(items)==2:
        cells = items[1].find_all('td')
        if len(cells)==171:
            for j in range(16):
                stt = cells[8+j*7].get_text()
                indicator = cells[8 + j * 7+1].get_text()
                i2017 = cells[8 + j * 7 + 2].get_text()
                i2016 = cells[8 + j * 7 + 3].get_text()
                i2015 = cells[8 + j * 7 + 4].get_text()
                i2014 = cells[8 + j * 7 + 5].get_text()
                i2013 = cells[8 + j * 7 + 6].get_text()
                newRow = pd.DataFrame([[source.ix[i]['Stock'],stt,indicator,i2017,i2016,i2015,i2014,i2013]],columns=['stock','STT','indicator','2017','2016','2015','2014','2013'])
                # newRow['indicator'] = newRow.apply(clean_text)

                df = pd.concat([df,newRow])
            for k in range(5):
                stt = cells[121 + k * 7].get_text()
                indicator = cells[121 + k * 7 + 1].get_text()
                i2017 = cells[121 + k * 7 + 2].get_text()
                i2016 = cells[121 + k * 7 + 3].get_text()
                i2015 = cells[121 + k * 7 + 4].get_text()
                i2014 = cells[121 + k * 7 + 5].get_text()
                i2013 = cells[121 + k * 7 + 6].get_text()
                newRow = pd.DataFrame([[source.ix[i]['Stock'], stt, indicator, i2017, i2016, i2015, i2014, i2013]],
                                      columns=['stock', 'STT', 'indicator', '2017', '2016', '2015', '2014', '2013'])
                # newRow['indicator'] = newRow.apply(clean_text)
                df = pd.concat([df, newRow])
            for l in range(2):
                stt = cells[157 + l * 7].get_text()
                indicator = cells[157 + l * 7 + 1].get_text()
                i2017 = cells[157 + l * 7 + 2].get_text()
                i2016 = cells[157 + l * 7 + 3].get_text()
                i2015 = cells[157 + l * 7 + 4].get_text()
                i2014 = cells[157 + l * 7 + 5].get_text()
                i2013 = cells[157 + l * 7 + 6].get_text()
                newRow = pd.DataFrame([[source.ix[i]['Stock'], stt, indicator, i2017, i2016, i2015, i2014, i2013]],
                                      columns=['stock', 'STT', 'indicator', '2017', '2016', '2015', '2014', '2013'])
                # newRow[newRow.apply(lambda x: x.str.contains('N/A'))] = 0
                # newRow['indicator'] = newRow.apply(clean_text)
                df = pd.concat([df, newRow])
        '''
        cells[2]: Q3 2017
        cells[3]: 2016
        cells[4]: 2015
        cells[5]: 2014
        cells[6]: 2013
        cells[9]: tai san ngan han/tong tai san
        cells[120]: ti le tang truong tai chinh 7*5
        cells[156]: ti le thu nhap 7*2

        '''
        # cells
        # cells[100]
df.to_csv('fundamental/cophieu68.csv',index=False, encoding='utf-8')