# Implement a P controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau_p * CTE - tau_d * diff_CTE - tau_i * int_CTE
#
# where the integrated crosstrack error (int_CTE) is
# the sum of all the previous crosstrack errors.
# This term works to cancel out steering drift.
# run - does a single control run.
from math import pi
from robot import robot

def run(param1, param2, param3):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    N = 100
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree bias, this will be added in by the move function, you do not need to add it below!
    
    setpoint = 0.0
    P = (myrobot.y - setpoint)
    I = 0.0
    
    for _ in range(N):
        D = myrobot.y - P
        P = (myrobot.y - setpoint)
        I += P
        steer = -param1 * P -param2 * D -param3 * I
        myrobot = myrobot.move(steer, speed)
        print myrobot, steer

# Call your function with parameters of (0.2, 3.0, and 0.004)
run(0.2, 3.0, 0.004)
