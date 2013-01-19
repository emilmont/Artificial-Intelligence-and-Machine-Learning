import copy
from datetime import datetime, timedelta
from numpy import NAN

import qenv
from qstkutil.qsdateutil import getNYSEdays
from qstkutil.DataAccess import DataAccess
from qstkstudy.EventProfiler import EventProfiler


dataobj = DataAccess('Yahoo')

THRESHOLD = 10

START_DAY = datetime(2008, 1, 1)
END_DAY   = datetime(2009, 12, 31)

# Survivorship Bias
# http://en.wikipedia.org/wiki/Survivorship_bias#In_finance
SYMBOLS_STOCK_YEAR = 2012 


def event(eventmat, sym, prices):
    for t in range(1, len(prices)):
        # The actual close of the stock price drops below $5.00
        if prices[t-1] >= THRESHOLD and prices[t] < THRESHOLD:
            eventmat[sym][t] = 1.0


def findEvents(symbols, startday, endday):
    # Reading the Data for the list of Symbols.
    timestamps = getNYSEdays(startday, endday, timedelta(hours=16))
    
    # Reading the Data
    print "# reading data"
    close = dataobj.get_data(timestamps, symbols, "actual_close")
    
    # Generating the Event Matrix
    print "# finding events"
    eventmat = copy.deepcopy(close)
    for sym in symbols:
        for time in timestamps:
            eventmat[sym][time] = NAN
    
    for symbol in symbols:
        event(eventmat, symbol, close[symbol])
    
    return eventmat


def run_analysis(year):
    event_name = "sp500%d" % year
    symbols = dataobj.get_symbols_from_list(event_name)
    symbols.append('SPY')
    
    eventMatrix = findEvents(symbols, START_DAY, END_DAY)
    
    print "# Event Profiler"
    eventProfiler = EventProfiler(eventMatrix, START_DAY, END_DAY,
                                     lookback_days=20, lookforward_days=20, verbose=True)
    
    print "# Plot"
    eventProfiler.study(filename="%s.pdf" % event_name,
                        plotErrorBars=True, plotMarketNeutral=True,
                        plotEvents=False, marketSymbol='SPY')


if __name__ == '__main__':
    run_analysis(SYMBOLS_STOCK_YEAR)
