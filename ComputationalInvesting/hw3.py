import csv
from datetime import date, datetime, timedelta
from collections import defaultdict

import qenv
from qstkutil.DataAccess import DataAccess
from qstkutil.qsdateutil import getNYSEdays
from hw1 import Equities


class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.shares = defaultdict(int)
    
    def update(self, sym, num, share_cost):
        self.cash -= num * share_cost
        self.shares[sym] += num
    
    def value(self, close, d):
        return self.cash + sum([num * close[sym][d] for sym, num in self.shares.iteritems()])


def marketsim(cash, orders_file, data_item):
    # Read orders
    orders = defaultdict(list)
    symbols = set([])
    for year, month, day, sym, action, num in csv.reader(open(orders_file, "rU")):
        orders[date(int(year), int(month), int(day))].append((sym, action, int(num)))
        symbols.add(sym)
    
    days = orders.keys()
    days.sort()
    day, end = days[0], days[-1]
    
    # Reading the Data for the list of Symbols.
    timestamps = getNYSEdays(datetime(day.year,day.month,day.day),
                             datetime(end.year,end.month,end.day+1),
                             timedelta(hours=16))
    
    dataobj = DataAccess('Yahoo')
    close = dataobj.get_data(timestamps, symbols, data_item)
    
    values = []
    portfolio = Portfolio(cash)
    for i, t in enumerate(timestamps):
        for sym, action, num in orders[date(t.year, t.month, t.day)]:
            if action == 'Sell': num *= -1
            portfolio.update(sym, num, close[sym][i])
        
        entry = (t.year, t.month, t.day, portfolio.value(close, i))
        values.append(entry)
    
    return values


def analyze(values):
    print Equities([v[3] for v in values], "Portfolio")


if __name__ == "__main__":
    CASH = 1000000
    ORDERS_FILE = "data/orders.csv"
    BENCHMARK = "$SPX"
    
    analyze(marketsim(CASH, ORDERS_FILE, "close"))
