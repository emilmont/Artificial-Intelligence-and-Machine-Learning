from scipy import polyfit, polyval, sqrt
from scipy import matrix, zeros, sum


def linear_regression(x, y):
    (w1, w0) = polyfit(x, y, 1)
    xr = polyval([w1, w0], y)
    err = sqrt(sum((xr - x)**2) / len(x))
    return (w0, w1), err


def gaussian(x):
    lines, columns = x.shape
    m = zeros(columns)
    for i in range(columns):
        m[i] = sum(x[:,i]) / lines
    
    diff = matrix(zeros((lines,columns)))
    for i in range(lines):
        diff[i,:] = x[i,:] - m
    s = (diff.T * diff) / lines
    
    return m, s
