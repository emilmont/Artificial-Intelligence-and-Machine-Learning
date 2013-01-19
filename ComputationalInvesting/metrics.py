from math import sqrt
from numpy import mean, std


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
