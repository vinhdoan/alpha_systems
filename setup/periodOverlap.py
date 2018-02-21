#!/usr/bin/env python3
from datetime import timedelta
import sys
import pandas as pd


def date_range(startDate, stopDate):
    for n in range((stopDate - startDate).days + 1):
        yield startDate + timedelta(n)


# List of pairs of pandas Timestamp expected
def to(*periods):
    d = {}
    for start, stop in periods:
        startDate = start.date()
        stopDate = stop.date()
        for aDay in date_range(startDate, stopDate):
            d[aDay] = d.get(aDay, 0) + 1
    invD = {}
    for k, v in d.items():
        invD[v] = invD.get(v, [])
        invD[v].append(k)
    m = max(invD.keys())
    return invD[m]


if __name__ == '__main__':
    data = pd.read_csv('testresults/52wksbreakout-buysellClose.csv', parse_dates=['buyDate', 'sellDate'])
    result = to(*list(zip(data['buyDate'], data['sellDate'])))
    print(result)