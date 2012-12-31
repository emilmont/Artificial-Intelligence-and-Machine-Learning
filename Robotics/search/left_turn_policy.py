# ----------
# User Instructions:
# 
# Implement the function optimum_policy2D() below.
#
# You are given a car in a grid with initial state
# init = [x-position, y-position, orientation]
# where x/y-position is its position in a given
# grid and orientation is 0-3 corresponding to 'up',
# 'left', 'down' or 'right'.
#
# Your task is to compute and return the car's optimal
# path to the position specified in `goal'; where
# the costs for each motion are as defined in `cost'.

# EXAMPLE INPUT:

# grid format:
#     0 = navigable space
#     1 = occupied space 
grid = [[1, 1, 1, 0, 0, 0],
        [1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1]]
goal = [2, 0] # final position
init = [4, 3, 0] # first 2 elements are coordinates, third is direction
cost = [2, 1, 20] # the cost field has 3 values: right turn, no turn, left turn

# EXAMPLE OUTPUT:
# calling optimum_policy2D() should return the array
# 
# [[' ', ' ', ' ', 'R', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', '#'],
#  ['*', '#', '#', '#', '#', 'R'],
#  [' ', ' ', ' ', '#', ' ', ' '],
#  [' ', ' ', ' ', '#', ' ', ' ']]
#
# ----------


# there are four motion directions: up/left/down/right
# increasing the index in this array corresponds to
# a left turn. Decreasing is is a right turn.

forward = [[-1,  0], # go up
           [ 0, -1], # go left
           [ 1,  0], # go down
           [ 0,  1]] # do right
forward_name = ['up', 'left', 'down', 'right']

# the cost field has 3 values: right turn, no turn, left turn
action = [-1, 0, 1]
action_name = ['R', '#', 'L']


# ----------------------------------------
# modify code below
# ----------------------------------------

def optimum_policy2D():
    value    = [[[999 for row in range(len(grid[0]))] for col in range(len(grid))],
                [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
                [[999 for row in range(len(grid[0]))] for col in range(len(grid))],
                [[999 for row in range(len(grid[0]))] for col in range(len(grid))]]
    policy   = [[[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
                [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
                [[' ' for row in range(len(grid[0]))] for col in range(len(grid))],
                [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]]
    
    policy2D = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    
    change = True
    while change:
        change = False
        
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                for orientation in range(4):
                    
                    if goal[0] == x and goal[1] == y:
                        if value[orientation][x][y] > 0:
                            value[orientation][x][y] = 0
                            policy[orientation][x][y] = '*'
                            change = True
                    
                    elif grid[x][y] == 0:
                        for a in range(len(action)):
                            o2 = (orientation + action[a]) % 4
                            x2 = x + forward[o2][0]
                            y2 = y + forward[o2][1]
                            
                            if (x2 >= 0 and x2 < len(grid)    and
                                y2 >= 0 and y2 < len(grid[0]) and
                                grid[x2][y2] == 0):
                                
                                v2 = value[o2][x2][y2] + cost[a]
                                
                                if v2 < value[orientation][x][y]:
                                    value[orientation][x][y] = v2
                                    policy[orientation][x][y] = action_name[a]
                                    change = True
    
    x = init[0]
    y = init[1]
    orientation = init[2]
    policy2D[x][y] = policy[orientation][x][y]
    while policy[orientation][x][y] != '*':
        if policy[orientation][x][y] == '#':
            o2 = orientation
        elif policy[orientation][x][y] == 'R':
            o2 = (orientation - 1) % 4
        elif policy[orientation][x][y] == 'L':
            o2 = (orientation + 1) % 4
        x = x + forward[o2][0]
        y = y + forward[o2][1]
        orientation = o2
        policy2D[x][y] = policy[orientation][x][y]
    
    return policy2D

for row in optimum_policy2D():
    print row

