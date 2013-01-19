# Setup the require environmental variables for QSTK
# http://wiki.quantsoftware.org/index.php?title=QuantSoftware_ToolKit
from os import environ
from os.path import join
from sys import path

HOME = '/home/emilmont'
QS = join(HOME, 'Software/QSTK')
QSDATA = join(HOME, 'Data/QSData')

environ.update({
    'QS'             : QS,
    'QSDATA'         : QSDATA,
    'QSDATAPROCESSED': join(QSDATA, 'Processed'),
    'QSDATATMP'      : join(QSDATA, 'Tmp'),
    'QSBIN'          : join(QS, 'Bin'),
    'QSSCRATCH'      : join(QSDATA, 'Scratch'),
    'CACHESTALLTIME' : '12',
})

path.append(QS)
