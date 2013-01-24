import copy
from datetime import datetime, timedelta
from numpy import NAN

import qenv
from qstkutil.qsdateutil import getNYSEdays
from qstkutil.DataAccess import DataAccess
from qstkstudy.EventProfiler import EventProfiler


def below_5_dollars_event(eventmat, sym, prices, timestamps):
    for t in range(1, len(prices)):
        # The actual close of the stock price drops below $5.00
        if prices[t-1] >= 5.00 and prices[t] < 5.00:
            eventmat[sym][t] = 1.0


def findEvents(symbols_year, startday, endday, event, data_item="close"):
    dataobj = DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list("sp500%d" % symbols_year)
    symbols.append('SPY')
    
    # Reading the Data for the list of Symbols.
    timestamps = getNYSEdays(startday, endday, timedelta(hours=16))
    
    # Reading the Data
    print "# reading data"
    close = dataobj.get_data(timestamps, symbols, data_item)
    
    # Generating the Event Matrix
    print "# finding events"
    eventmat = copy.deepcopy(close)
    for sym in symbols:
        for time in timestamps:
            eventmat[sym][time] = NAN
    
    for symbol in symbols:
        event(eventmat, symbol, close[symbol], timestamps)
    
    return eventmat


if __name__ == '__main__':
    START_DAY = datetime(2008,  1,  1)
    END_DAY   = datetime(2009, 12, 31)
    
    # Survivorship Bias
    # http://en.wikipedia.org/wiki/Survivorship_bias#In_finance
    SYMBOLS_STOCK_YEAR = 2012
    
    eventMatrix = findEvents(SYMBOLS_STOCK_YEAR, START_DAY, END_DAY,
                             below_5_dollars_event, "actual_close")
    
    print "# Event Profiler"
    eventProfiler = EventProfiler(eventMatrix, START_DAY, END_DAY,
                                     lookback_days=20, lookforward_days=20, verbose=True)
    
    print "# Plot"
    eventProfiler.study(filename="data/event.pdf",
                        plotErrorBars=True, plotMarketNeutral=True,
                        plotEvents=False, marketSymbol='SPY')
