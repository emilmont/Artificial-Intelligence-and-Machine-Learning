from datetime import datetime, timedelta
from math import sqrt
from numpy import mean, std

import qenv
from qstkutil.DataAccess import DataAccess
from qstkutil.qsdateutil import getNYSEdays


class Equities:
    def __init__(self, values, name=None):
        self.values = values
        self.name = name
        self.returns = map(self.single_return, range(1, len(self.values)))
    
    def roi(self, start, end):
        if self.values[end] == self.values[start]: return 0
        return (self.values[end] / self.values[start]) - 1
    
    def tot_return(self):
        return self.roi(0, -1)
    
    def single_return(self, d):
        return self.roi(d-1, d)
    
    def average_return(self):
        return mean(self.returns)
    
    def stdev_return(self):
        return std(self.returns)
    
    def sharpe_ratio(self):
        return (self.average_return() / self.stdev_return()) * sqrt(len(self.values))
    
    def __str__(self):
        return '\n'.join([
            "\n[%s]" % (self.name if self.name is not None else "Equities"),
            "Sharpe Ratio     : %.6f" % self.sharpe_ratio(),
            "Total Return     : %.4f" % self.tot_return(),
            "Average Daily Ret: %.6f" % self.average_return(),
            "STDEV Daily Ret  : %.6f" % self.stdev_return(),
        ])


if __name__ == '__main__':
    # TODO: sharp ratio higher than 4?
    PORTFOLIO = (
        ('AAPL' , 0.6),
        ('GLD'  , 0.2),
        ('WMT'  , 0.1),
        ('CVX'  , 0.1)
    )
    
    YEAR = 2011
    timestamps = getNYSEdays(datetime(YEAR,  1,  1),
                             datetime(YEAR, 12, 31),
                             timedelta(hours=16))
    
    BENCHMARK = 'SPY'
    symbols = [s for s, _ in PORTFOLIO] + [BENCHMARK]
    
    close = DataAccess('Yahoo').get_data(timestamps, symbols, "close")
    
    print Equities([sum([close[s][i] for s in symbols]) for i in range(len(timestamps))], "Portfolio")
    print Equities([     close[BENCHMARK][i]            for i in range(len(timestamps))], "Benchmark")
