# Implement twiddle as shown in the previous two videos.
# Your accumulated error should be very small!
#
# Your twiddle function should RETURN the accumulated
# error. Try adjusting the parameters p and dp to make
# this error as small as possible.
#
# Try to get your error below 1.0e-10 with as few iterations
# as possible (too many iterations will cause a timeout).
from math import pi
from robot import robot

# run - does a single control run.
def run(params, printflag = False):
    myrobot = robot()
    myrobot.set(0.0, 1.0, 0.0)
    speed = 1.0
    err = 0.0
    int_crosstrack_error = 0.0
    N = 100
    # myrobot.set_noise(0.1, 0.0)
    myrobot.set_steering_drift(10.0 / 180.0 * pi) # 10 degree steering error


    crosstrack_error = myrobot.y


    for i in range(N * 2):

        diff_crosstrack_error = myrobot.y - crosstrack_error
        crosstrack_error = myrobot.y
        int_crosstrack_error += crosstrack_error

        steer = - params[0] * crosstrack_error  \
            - params[1] * diff_crosstrack_error \
            - int_crosstrack_error * params[2]
        myrobot = myrobot.move(steer, speed)
        if i >= N:
            err += (crosstrack_error ** 2)
        if printflag:
            print myrobot, steer
    return err / float(N)


def twiddle(tol = 0.001): #Make this tolerance bigger if you are timing out!
    n_params = 3
    params  = [0.0] * n_params
    dparams = [1.0] * n_params
    
    best_error = run(params)
    n = 0
    while sum(dparams) > tol:
        for i in range(n_params):
            params[i] += dparams[i]
            err = run(params)
            if err < best_error:
                best_error = err
                dparams[i] *= 1.1
            else:
                params[i] -= 2.0 * dparams[i]
                err = run(params)
                if err < best_error:
                    best_error = err
                    dparams[i] * 1.1
                else:
                    params[i] += dparams[i]
                    dparams[i] *= 0.9
        n+= 1
        print "Twiddle #", n, params, ' -> ', best_error
    
    return run(params)

twiddle()
