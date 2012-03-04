R, G = 'red', 'green'

def show(p):
    for i in range(len(p)):
        print p[i]

colors = [[R, G, G, R, R],
          [R, R, G, R, R],
          [R, R, G, G, R],
          [R, R, R, R, R]]

measurements = [G, G, G, G, G]
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7
p_move = 0.8

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT
pHit, pMiss = sensor_right, (1 - sensor_right)
pMove, pStill = p_move, (1 - p_move)

def matrix(rows, columns, init=0):
    return [[init]*columns for _ in range(rows)]

def uniform_matrix(rows, columns):
    prob = 1. / (rows * columns)
    return matrix(rows, columns, prob)

def size_matrix(world):
    return len(world), len(world[0])

def sum_matrix(m):
    s = 0.
    for row in m:
        s += sum(row) 
    return s

def sense(p, Z):
    n_rows, n_columns = size_matrix(p)
    
    # Add sensor information
    for i in range(n_rows):
        for j in range(n_columns):
            p[i][j] *= (pHit if colors[i][j] == Z else pMiss)
    
    # Normalise
    s = sum_matrix(p)
    for i in range(n_rows):
        for j in range(n_columns):
            p[i][j] /= s

def move(p, U):
    i_delta, j_delta = U
    n_rows, n_columns = size_matrix(p)
    q = matrix(n_rows, n_columns)
    
    for i in range(n_rows):
        for j in range(n_columns):
            i_move = (i - i_delta) % n_rows
            j_move = (j - j_delta) % n_columns
            q[i][j] = (pMove  * p[i_move][j_move] + pStill * p[i][j])
    
    return q

p = uniform_matrix(*size_matrix(colors))
for i in range(len(motions)):
    p = move(p, motions[i])
    sense(p, measurements[i])

#Your probability array must be printed 
#with the following code.
show(p)
