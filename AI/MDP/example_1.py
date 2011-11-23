from MDP.grid import GridWorld

GRID = [[0,    0, 0,  100],
        [0, None, 0, -100],
        [0,    0, 0,    0]]

PROB = {
    'S':(('S', 0.8), ('W', 0.1), ('E', 0.1)),
    'N':(('N', 0.8), ('E', 0.1), ('W', 0.1)),
    'E':(('E', 0.8), ('S', 0.1), ('N', 0.1)),
    'W':(('W', 0.8), ('N', 0.1), ('S', 0.1)),
}

STATES = ((0,2),(0,1),(1,2),(0,0),(2,2),(1,0),(2,1),(2,0),(2,3))

if __name__ == '__main__':
    g = GridWorld(GRID, PROB, STATES, 1, -3)
    v = g.value(0,2)
    print "\nValue of (0,2) after first iteration: %.1f" % v
    g.grid[0][2] = v
    print "\nValue of (1,2) after first iteration: %.1f" % g.value(1,2)
    
    print "\nInitial values:"
    g = GridWorld(GRID, PROB, STATES, 1, -3)
    print g
    
    i = g.value_iteration(0.1)
    print "\nValues after %d iterations:" % i
    print g
