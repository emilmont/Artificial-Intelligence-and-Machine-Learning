from datetime import datetime, timedelta


import qenv
from qstkutil.DataAccess import DataAccess
from qstkutil.qsdateutil import getNYSEdays
from metrics import Equities


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
