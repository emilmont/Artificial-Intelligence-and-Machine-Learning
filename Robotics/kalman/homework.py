from matrix import matrix


def filter(x, P):
    for n in range(len(measurements)):
        
        # prediction
        x = (F * x) + u
        P = F * P * F.transpose()
        
        # measurement update
        Z = matrix([measurements[n]])
        y = Z.transpose() - (H * x)
        S = H * P * H.transpose() + R
        K = P * H.transpose() * S.inverse()
        x = x + (K * y)
        P = (I - (K * H)) * P
    
    print 'x= '
    x.show()
    print 'P= '
    P.show()


########################################
print "### 4-dimensional example ###"

measurements = [[5., 10.], [6., 8.], [7., 6.], [8., 4.], [9., 2.], [10., 0.]]
initial_xy = [4., 12.]

# measurements = [[1., 4.], [6., 0.], [11., -4.], [16., -8.]]
# initial_xy = [-4., 8.]

# measurements = [[1., 17.], [1., 15.], [1., 13.], [1., 11.]]
# initial_xy = [1., 19.]

# measurements = [[2., 17.], [0., 15.], [2., 13.], [0., 11.]]
# initial_xy = [1., 19.]

dt = 0.1

x = matrix([[initial_xy[0]], [initial_xy[1]], [0.], [0.]]) # initial state (location and velocity)
u = matrix([[0.], [0.], [0.], [0.]]) # external motion

P = matrix([[0., 0., 0., 0.],
            [0., 0., 0., 0.],
            [0., 0., 1000., 0.],
            [0., 0., 0., 1000.]]) # initial uncertainty
F = matrix([[1., 0., 0.1, 0. ],
            [0., 1., 0. , 0.1],
            [0., 0., 1. , 0. ],
            [0., 0., 0. , 1. ]]) # next state function
H = matrix([[1., 0., 0., 0.],
            [0., 1., 0., 0.]]) # measurement function
R = matrix([[0.1, 0. ],
            [0. , 0.1]]) # measurement uncertainty
I = matrix([[1., 0., 0., 0.],
            [0., 1., 0., 0.],
            [0., 0., 1., 0.],
            [0., 0., 0., 1.]]) # identity matrix

filter(x, P)
