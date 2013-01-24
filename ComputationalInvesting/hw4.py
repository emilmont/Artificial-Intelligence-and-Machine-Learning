"""
Use the actual close $5.00 event with the 2012 SP500 data.

I expect that this strategy should make money.
Use the following parameters:
  * Starting cash: $50,000
  * Start date: 1 January 2008
  * End date: 31 December 2009
  * When an event occurs, buy 100 shares of the equity on that day.
  * Sell automatically 5 trading days later.

Compute the Sharpe Ratio, total return and STDDEV of daily returns.
"""
from datetime import datetime

from hw2 import findEvents
from hw3 import marketsim, analyze


class EventStrategy:
    def __init__(self, order_file, threshold, num, hold_days):
        self.f = open(order_file, "w")
        self.threshold = threshold
        self.num = num
        self.hold_days = hold_days
        
    
    def add_order(self, timestamp, sym, action, num):
        self.f.write(",".join(map(str, [
            timestamp.year, timestamp.month, timestamp.day,
            sym, action, num
        ])) + "\n")
    
    def threshold_event(self, eventmat, sym, prices, timestamps):
        for t in range(1, len(prices)):
            # The actual close of the stock price drops below a given threshold
            if prices[t-1] >= self.threshold and prices[t] < self.threshold:
                eventmat[sym][t] = 1.0
                self.add_order(timestamps[t               ], sym, "Buy" , self.num)
                self.add_order(timestamps[t+self.hold_days], sym, "Sell", self.num)
    
    def close(self):
        self.f.close()


if __name__ == "__main__":
    START_DAY = datetime(2008,  1,  1)
    END_DAY   = datetime(2009, 12, 31)
    SYMBOLS_STOCK_YEAR = 2012
    THRESHOLD = 7
    CASH = 100000
    ORDERS_FILE = "data/orders_event.csv"
    BUY_N = 100
    HOLD_DAYS = 5
    CLOSE_TYPE = "actual_close"
    
    strategy = EventStrategy(ORDERS_FILE, THRESHOLD, BUY_N, HOLD_DAYS)
    findEvents(SYMBOLS_STOCK_YEAR, START_DAY, END_DAY,
               strategy.threshold_event, "actual_close")
    strategy.close()
    
    analyze(marketsim(CASH, ORDERS_FILE, "close"))
