# Modify your doit function to incorporate 3
# distance measurements to a landmark(Z0, Z1, Z2).
# You should use the provided expand function to
# allow your Omega and Xi matrices to accomodate
# the new information.
#
# Each landmark measurement should modify 4
# values in your Omega matrix and 2 in your
# Xi vector.
from matrix import matrix

"""
For the following example, you would call doit(-3, 5, 3, 10, 5, 2):
3 robot positions
  initially: -3 (measure landmark to be 10 away)
  moves by 5 (measure landmark to be 5 away)
  moves by 3 (measure landmark to be 2 away)

  

which should return a mu of:
[[-3.0],
 [2.0],
 [5.0],
 [7.0]]
"""
# Including the 5 times multiplier, your returned mu should now be:
#
# [[-3.0],
#  [2.179],
#  [5.714],
#  [6.821]]

def doit(initial_pos, move1, move2, Z0, Z1, Z2):
    # initial_position:
    Omega = matrix([[1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0]])
    Xi = matrix([[initial_pos],
                 [0.0],
                 [0.0]])
    
    # move1
    Omega += matrix([[1.0, -1.0, 0.0],
                     [-1.0, 1.0, 0.0],
                     [0.0, 0.0, 0.0]])
    Xi += matrix([[-move1],
                  [move1],
                  [0.0]])
    
    # move2
    Omega += matrix([[0.0, 0.0, 0.0],
                     [0.0, 1.0, -1.0],
                     [0.0, -1.0, 1.0]])
    Xi += matrix([[0.0],
                  [-move2],
                  [move2]])
    
    # expand
    Omega = Omega.expand(Omega.dimx + 1, Omega.dimy + 1, range(Omega.dimx))
    Xi = Xi.expand(Xi.dimx + 1, Xi.dimy, range(Xi.dimx), [0])
    
    # first measurement:
    Omega += matrix([[1.0, 0.0, 0.0, -1.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [-1.0, 0.0, 0.0, 1.0]])
    Xi    += matrix([[-Z0],
                     [0.0],
                     [0.0],
                     [Z0]])

    Omega += matrix([[0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0, 0.0, -1.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, -1.0, 0.0, 1.0]])
    Xi    += matrix([[0.0],
                     [-Z1],
                     [0.0],
                     [Z1]])
    
    # third measurement:
    Omega += matrix([[0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 5.0, -5.0],
                     [0.0, 0.0, -5.0, 5.0]])
    Xi    += matrix([[0.0],
                     [0.0],
                     [-5*Z2],
                     [5*Z2]])

    Omega.show('Omega: ')
    Xi.show('Xi:    ')
    mu = Omega.inverse() * Xi
    mu.show('Mu:    ')
    
    return mu

doit(-3, 5, 3, 10, 5, 1)


def matrix_fill_in(initial_pos, move_sigma, move1, move2, measure_sigma, Z0, Z1, Z2):
    # initial position:
    Omega = matrix([[1.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0, 0.0, 0.0]])
    Xi    = matrix([[initial_pos],
                    [0.0],
                    [0.0],
                    [0.0],
                    [0.0]])

    # move 1:
    Omega += matrix([[1.0/move_sigma, -1.0/move_sigma, 0.0, 0.0, 0.0],
                     [-1.0/move_sigma, 1.0/move_sigma, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    Xi    += matrix([[-move1/move_sigma],
                     [move1/move_sigma],
                     [0.0],
                     [0.0],
                     [0.0]])
    
    # move 2:
    Omega += matrix([[0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0/move_sigma, -1.0/move_sigma, 0.0, 0.0],
                     [0.0, -1.0/move_sigma, 1.0/move_sigma, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    Xi    += matrix([[0.0],
                     [-move2/move_sigma],
                     [move2/move_sigma],
                     [0.0],
                     [0.0]])
    
    # measure 0
    Omega += matrix([[1.0/measure_sigma, 0.0, 0.0, -1.0/measure_sigma, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [-1.0/measure_sigma, 0.0, 0.0, 1.0/measure_sigma, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0]])
    
    Xi    += matrix([[-Z0/measure_sigma],
                     [0.0],
                     [0.0],
                     [Z0/measure_sigma],
                     [0.0]])
    
    # measure 1
    Omega += matrix([[0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 1.0/measure_sigma, 0.0, 0.0, -1.0/measure_sigma],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, -1.0/measure_sigma, 0.0, 0.0, 1.0/measure_sigma]])
    Xi    += matrix([[0.0],
                     [-Z1/measure_sigma],
                     [0.0],
                     [0.0],
                     [Z1/measure_sigma]])
    
    # measure 2
    Omega += matrix([[0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 1.0/measure_sigma, 0.0, -1.0/measure_sigma],
                     [0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, -1.0/measure_sigma, 0.0, 1.0/measure_sigma]])
    Xi    += matrix([[0.0],
                     [0.0],
                     [-Z2/measure_sigma],
                     [0.0],
                     [Z2/measure_sigma]])
    
    Omega.show('Omega: ')
    Xi.show('Xi:    ')
    mu = Omega.inverse() * Xi
    mu.show('Mu:    ')
    
    return mu

initial_pos = 5
move_sigma = 1
move0 = 7
move1 = 2
measure_sigma = 0.5
measure0 = 2
measure1 = 4
measure2 = 2
matrix_fill_in(initial_pos, move_sigma, move0, move1, measure_sigma, measure0, measure1, measure2)