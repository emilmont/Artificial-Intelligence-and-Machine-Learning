from numpy import array
from ComputerVision.filters import linear_filter, linear_filter_hw

image = array([
    [255,   7,   3],
    [212, 240,   4],
    [218, 216, 230],
])
print linear_filter(image, ((0,1),(-1, 1)))

image = array([
    [ 12,  18,   6],
    [  2,   1,   7],
    [100, 140, 130],
])
print linear_filter(image, ((1,0), (-1, 1)))

image = array([
    [2,   0,   2],
    [4, 100, 102],
    [2,   4,   2],
])
print linear_filter_hw(image, (-1, 0, 1))