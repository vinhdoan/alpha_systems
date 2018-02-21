from zipline.api import order_target, record, symbol, order
from zipline import TradingAlgorithm
from collections import OrderedDict
import pandas as pd
import pytz
from datetime import datetime
from zipline.algorithm import TradingAlgorithm
import zipline
import pyexcel
from pandas.tseries.offsets import *

start = datetime(2012,1,1)
end = datetime(2017,1,1)

def initialize(context):
    context.security = symbol('VNM')
    context.count = 1


def handle_data(context, data):
    # Skip first 100 days to get full windows
    context.count += 1
    if context.count<200:
        return
    else:
        if data[context.security].close == 0:
            return
        else:
            #order(symbol('VNM'), 10)
            record(VNM=data.current(symbol('VNM'), 'price'))
            MA1 = data[context.security].mavg(50)
            MA2 = data[context.security].mavg(100)
            date = str(data[context.security].datetime)[:100]
            print(date)
            current_price = data[context.security].price
            current_positions = context.portfolio.positions[symbol('VNM')].amount
            cash = context.portfolio.cash
            value = context.portfolio.portfolio_value
            current_pnl = context.portfolio.pnl

            # code (this will come under handle_data function only)
            if (MA1 > MA2) and current_positions == 0:
                number_of_shares = int(cash / current_price)
                order(context.security, number_of_shares)
                record(date=date, MA1=MA1, MA2=MA2, Price=
                current_price, status="buy", shares=number_of_shares, PnL=current_pnl, cash=cash, value=value)

            elif (MA1 < MA2) and current_positions != 0:
                order_target(context.security, 0)
                record(date=date, MA1=MA1, MA2=MA2, Price=current_price, status="sell", shares="--", PnL=current_pnl, cash=cash,
                       value=value)

            # else:
            #     record(date=date, MA1=MA1, MA2=MA2, Price=current_price, status="--", shares="--", PnL=current_pnl, cash=cash,
            #            value=value)


data = OrderedDict()
data['VNM'] = pd.read_csv('data/VNM.csv',index_col =0, parse_dates=['Date'])
data['VNM'].columns = ['open','high', 'low', 'close', 'volume']
data['VNM']['price'] = data['VNM']['close']
data['VNM'] = data['VNM'].resample('B').sum()
data['VNM'].fillna(0)
#data['VNM'] = data['VNM'].reset_index()
panel = pd.Panel(data)
panel.minor_axis = ['open', 'high', 'low', 'close', 'volume', 'price']
panel.major_axis = panel.major_axis.tz_localize(pytz.utc)
#initializing
algo_obj = TradingAlgorithm(initialize=initialize, handle_data=handle_data)
#runalgo
perf_manual = algo_obj.run(panel)

perf_manual =  algo_obj.run_algorithm(start,end,initialize,capital_base=10000000,data=panel)


print(perf_manual)
#print(algo_obj)


#code
#calculation
# print("total pnl : " + str(float(perf_manual[["PnL"]].iloc[-1])))
# buy_trade = perf_manual[["status"]].loc[perf_manual["status"] == "buy"].count()
# sell_trade = perf_manual[["status"]].loc[perf_manual["status"] == "sell"].count()
# total_trade = buy_trade + sell_trade
# print("buy trade : " + str(int(buy_trade)) + " sell trade : " + str(int(sell_trade)) + " total trade : " + str(int(total_trade)))
# perf_manual[["MA1","MA2","Price"]].plot()
