from MDP.grid import GridWorld

GRID = [[   0, 0, 0,   0],
        [-100, 0, 0, 100]]

def prob(p):
    p = float(p)
    n = 1.0 - p
    return {
        'S':(('S', p), ('N', n)),
        'N':(('N', p), ('S', n)),
        'E':(('E', p), ('W', n)),
        'W':(('W', p), ('E', n)),
    }

STATES = ((0,3),(0,2),(1,2),(0,1),(1,1),(0,0))

if __name__ == '__main__':
    print "\nInitial values:"
    g = GridWorld(GRID, prob(1), STATES, 1, -4)
    print g
    
    i = g.value_iteration(0.1)
    print "\nValues after %d iterations:" % i
    print g
    
    g = GridWorld(GRID, prob(0.8), STATES, 1, -4)
    print "\nValue of (1,2) after first iteration: %.1f" % g.value(0,3)
    
    g = GridWorld(GRID, prob(0.8), STATES, 1, -4)
    i = g.value_iteration(0.1)
    print "\nValues after %d iterations:" % i
    print g

