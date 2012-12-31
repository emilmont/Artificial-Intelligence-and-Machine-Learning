# Implement a P controller by running 100 iterations
# of robot motion. The steering angle should be set
# by the parameter tau so that:
#
# steering = -tau * crosstrack_error
#
# Note that tau is called "param" in the function
# run to be completed below.
#
# Your code should print output that looks like
# the output shown in the video. That is, at each step:
# print myrobot, steering
from robot import robot

# run - does a single control run
def run(param):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0 # motion distance is equal to speed (we assume time = 1)
    N = 100
    
    setpoint = 0.0
    for _ in range(N):
        P = (myrobot.y - setpoint)
        steer = -param * P
        myrobot = myrobot.move(steer, speed)
        print myrobot, steer

run(0.1) # call function with parameter tau of 0.1 and print results
