import pandas as pd
import numpy as np

def p2f(x):
    return float(x.strip('%'))/100

npm = pd.read_csv('fundamental/eps.csv')
# df = pd.read_csv('fundamental/cophieu68.csv', sep='\s+', converters={'col':p2f})
# npm = df.loc[df.indicator=="Lợi nhuận sau thuế/Vốn chủ sở hữu (ROE)"]
# npm = npm.reset_index(drop=True)
# npm.to_csv('fundamental/roe.csv')
# npm['2017'] = npm['2017'].apply(lambda x: x[:-1].replace(",","")).astype(float)/100
#
# npm['2016'] = npm['2016'].apply(lambda x: x[:-1]).replace(",","").astype(float)/100
#
# npm['2015'] = npm['2015'].apply(lambda x: x[:-1]).replace(",","").astype(float)/100
#
# npm['2014'] = npm['2014'].apply(lambda x: x[:-1]).replace(",","").astype(float)/100
#
# npm['2013'] = npm['2013'].apply(lambda x: x[:-1]).replace(",","").astype(float)/100

a = []
for i in range(len(npm)):
    if npm.ix[i]['2016'] > 0.5 and npm.ix[i]['2015'] > 0 and npm.ix[i]['2014'] > 0:
        print(npm.ix[i]['stock'], npm.ix[i]['2016'])
        a.append(npm.ix[i]['stock'])

print(a)