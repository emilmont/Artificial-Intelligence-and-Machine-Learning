# In this problem you will implement a more manageable
# version of graph SLAM in 2 dimensions. 
#
# Define a function, online_slam, that takes 5 inputs:
# data, N, num_landmarks, motion_noise, and
# measurement_noise--just as was done in the last 
# programming assignment of unit 6. This function
# must return TWO matrices, mu and the final Omega.
#
# Just as with the quiz, your matrices should have x
# and y interlaced, so if there were two poses and 2
# landmarks, mu would look like:
#
# mu = matrix([[Px0],
#              [Py0],
#              [Px1],
#              [Py1],
#              [Lx0],
#              [Ly0],
#              [Lx1],
#              [Ly1]])
#
# Enter your code at line 566.

# -----------
# Testing
#
# You have two methods for testing your code.
#
# 1) You can make your own data with the make_data
#    function. Then you can run it through the
#    provided slam routine and check to see that your
#    online_slam function gives the same estimated
#    final robot pose and landmark positions.
# 2) You can use the solution_check function at the
#    bottom of this document to check your code
#    for the two provided test cases. The grading
#    will be almost identical to this function, so
#    if you pass both test cases, you should be
#    marked correct on the homework.
from matrix import matrix
from robot import robot, make_data, print_result, solution_check
from slam import slam

# --------------------------------
#
# online_slam - retains all landmarks but only most recent robot pose
#
def online_slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise):
    # Set the dimension of the filter
    dim = 2 * (1 + num_landmarks)
    
    # make the constraint information matrix and vector
    Omega = matrix()
    Omega.zero(dim, dim)
    Omega.value[0][0] = 1.0
    Omega.value[1][1] = 1.0
    
    Xi = matrix()
    Xi.zero(dim, 1)
    Xi.value[0][0] = world_size / 2.0
    Xi.value[1][0] = world_size / 2.0
    
    # process the data
    for k in range(len(data)):
        measurement = data[k][0]
        motion      = data[k][1]
        
        # integrate the measurements
        for i in range(len(measurement)):
            # m is the index of the landmark coordinate in the matrix/vector
            m = 2 * (1 + measurement[i][0])
            
            # update the information maxtrix/vector based on the measurement
            for b in range(2):
                Omega.value[b][b]     +=  1.0 / measurement_noise
                Omega.value[m+b][m+b] +=  1.0 / measurement_noise
                Omega.value[b][m+b]   += -1.0 / measurement_noise
                Omega.value[m+b][b]   += -1.0 / measurement_noise
                Xi.value[b][0]        += -measurement[i][1+b] / measurement_noise
                Xi.value[m+b][0]      +=  measurement[i][1+b] / measurement_noise
        
        #expand the information matrix and vector ny one new position
        list = [0, 1] + range(4, dim+2)
        Omega = Omega.expand(dim+2, dim+2, list, list)
        Xi    = Xi.expand(dim+2, 1, list, [0])
        
        # update the information maxtrix/vector based on the robot motion
        for b in range(4):
            Omega.value[b][b]     +=  1.0 / motion_noise
        for b in range(2):
            Omega.value[b  ][b+2] += -1.0 / motion_noise
            Omega.value[b+2][b  ] += -1.0 / motion_noise
            Xi.value[b  ][0]      += -motion[b] / motion_noise
            Xi.value[b+2][0]      +=  motion[b] / motion_noise
        
        # now factor out the previous pose
        newlist = range(2, len(Omega.value))
        a = Omega.take([0, 1], newlist)
        b = Omega.take([0, 1])
        c = Xi.take([0, 1], [0])
        
        Omega = Omega.take(newlist)   - a.transpose() * b.inverse() * a
        Xi    = Xi.take(newlist, [0]) - a.transpose() * b.inverse() * c
    
    # compute best estimate
    mu = Omega.inverse() * Xi
    return mu, Omega


# ------------------------------------------------------------------------
#
# Main routine
#
if __name__ == '__main__':
    num_landmarks      = 5        # number of landmarks
    N                  = 20       # time steps
    world_size         = 100.0    # size of world
    measurement_range  = 50.0     # range at which we can sense landmarks
    motion_noise       = 2.0      # noise in robot motion
    measurement_noise  = 2.0      # noise in the measurements
    distance           = 20.0     # distance by which robot (intends to) move each iteratation 
    
    # Run the full slam routine.
    data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
    result = slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)
    print_result(N, num_landmarks, result)
    
    # Run the online_slam routine.
    data = make_data(N, num_landmarks, world_size, measurement_range, motion_noise, measurement_noise, distance)
    result = online_slam(data, N, num_landmarks, world_size, motion_noise, measurement_noise)
    print_result(1, num_landmarks, result[0])
    
    # -----------
    # Test Case 1
    testdata1          = [[[[1, 21.796713239511305, 25.32184135169971], [2, 15.067410969755826, -27.599928007267906]], [16.4522379034509, -11.372065246394495]],
                          [[[1, 6.1286996178786755, 35.70844618389858], [2, -0.7470113490937167, -17.709326161950294]], [16.4522379034509, -11.372065246394495]],
                          [[[0, 16.305692184072235, -11.72765549112342], [2, -17.49244296888888, -5.371360408288514]], [16.4522379034509, -11.372065246394495]],
                          [[[0, -0.6443452578030207, -2.542378369361001], [2, -32.17857547483552, 6.778675958806988]], [-16.66697847355152, 11.054945886894709]]]
    
    answer_mu1         = matrix([[81.63549976607898],
                                 [27.175270706192254],
                                 [98.09737507003692],
                                 [14.556272940621195],
                                 [71.97926631050574],
                                 [75.07644206765099],
                                 [65.30397603859097],
                                 [22.150809430682695]])
    
    answer_omega1      = matrix([[0.36603773584905663, 0.0, -0.169811320754717, 0.0, -0.011320754716981133, 0.0, -0.1811320754716981, 0.0],
                                 [0.0, 0.36603773584905663, 0.0, -0.169811320754717, 0.0, -0.011320754716981133, 0.0, -0.1811320754716981],
                                 [-0.169811320754717, 0.0, 0.6509433962264151, 0.0, -0.05660377358490567, 0.0, -0.40566037735849064, 0.0],
                                 [0.0, -0.169811320754717, 0.0, 0.6509433962264151, 0.0, -0.05660377358490567, 0.0, -0.40566037735849064],
                                 [-0.011320754716981133, 0.0, -0.05660377358490567, 0.0, 0.6962264150943396, 0.0, -0.360377358490566, 0.0],
                                 [0.0, -0.011320754716981133, 0.0, -0.05660377358490567, 0.0, 0.6962264150943396, 0.0, -0.360377358490566],
                                 [-0.1811320754716981, 0.0, -0.4056603773584906, 0.0, -0.360377358490566, 0.0, 1.2339622641509433, 0.0],
                                 [0.0, -0.1811320754716981, 0.0, -0.4056603773584906, 0.0, -0.360377358490566, 0.0, 1.2339622641509433]])
    
    result = online_slam(testdata1, 5, 3, world_size, 2.0, 2.0)
    solution_check(result, answer_mu1, answer_omega1)
    
    # -----------
    # Test Case 2
    testdata2          = [[[[0, 12.637647070797396, 17.45189715769647], [1, 10.432982633935133, -25.49437383412288]], [17.232472057089492, 10.150955955063045]],
                          [[[0, -4.104607680013634, 11.41471295488775], [1, -2.6421937245699176, -30.500310738397154]], [17.232472057089492, 10.150955955063045]],
                          [[[0, -27.157759429499166, -1.9907376178358271], [1, -23.19841267128686, -43.2248146183254]], [-17.10510363812527, 10.364141523975523]],
                          [[[0, -2.7880265859173763, -16.41914969572965], [1, -3.6771540967943794, -54.29943770172535]], [-17.10510363812527, 10.364141523975523]],
                          [[[0, 10.844236516370763, -27.19190207903398], [1, 14.728670653019343, -63.53743222490458]], [14.192077112147086, -14.09201714598981]]]
    
    answer_mu2         = matrix([[63.37479912250136],
                                 [78.17644539069596],
                                 [61.33207502170053],
                                 [67.10699675357239],
                                 [62.57455560221361],
                                 [27.042758786080363]])
    
    answer_omega2      = matrix([[0.22871751620895048, 0.0, -0.11351536555795691, 0.0, -0.11351536555795691, 0.0],
                                 [0.0, 0.22871751620895048, 0.0, -0.11351536555795691, 0.0, -0.11351536555795691],
                                 [-0.11351536555795691, 0.0, 0.7867205207948973, 0.0, -0.46327947920510265, 0.0],
                                 [0.0, -0.11351536555795691, 0.0, 0.7867205207948973, 0.0, -0.46327947920510265],
                                 [-0.11351536555795691, 0.0, -0.46327947920510265, 0.0, 0.7867205207948973, 0.0],
                                 [0.0, -0.11351536555795691, 0.0, -0.46327947920510265, 0.0, 0.7867205207948973]])
    
    result = online_slam(testdata2, 6, 2, world_size, 3.0, 4.0)
    solution_check(result, answer_mu2, answer_omega2)
