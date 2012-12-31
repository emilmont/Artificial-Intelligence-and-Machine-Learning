# Implement a PD controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau_p * CTE - tau_d * diff_CTE
# where differential crosstrack error (diff_CTE)
# is given by CTE(t) - CTE(t-1)
from robot import robot

# run - does a single control run.
def run(param1, param2):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    N = 100
    
    setpoint = 0.0
    P = (myrobot.y - setpoint)
    
    for _ in range(N):
        D = myrobot.y - P
        P = (myrobot.y - setpoint)
        steer = -param1 * P -param2 * D
        myrobot = myrobot.move(steer, speed)
        print myrobot, steer

# Call your function with parameters of 0.2 and 3.0 and print results
run(0.2, 3.0)
