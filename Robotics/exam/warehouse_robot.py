# In this problem, you will build a planner that helps a robot
# find the shortest way in a warehouse filled with boxes
# that he has to pick up and deliver to a drop zone.
#
# For example:
#    warehouse = [[ 1, 2, 3],
#                 [ 0, 0, 0],
#                 [ 0, 0, 0]]
#    
#    dropzone = [2, 0] 
#    todo = [2, 1]
#
# Robot starts at the dropzone.
# Dropzone can be in any free corner of the warehouse map.
# todo is a list of boxes to be picked up and delivered to dropzone.
# Robot can move diagonally, but the cost of diagonal move is 1.5 
# Cost of moving one step horizontally or vertically is 1.0
# If the dropzone is at [2, 0], the cost to deliver box number 2
# would be 5.

# To pick up a box, robot has to move in the same cell with the box.
# When a robot picks up a box, that cell becomes passable (marked 0)
# Robot can pick up only one box at a time and once picked up 
# he has to return it to the dropzone by moving on to the cell.
# Once the robot has stepped on the dropzone, his box is taken away
# and he is free to continue with his todo list.
# Tasks must be executed in the order that they are given in the todo.
# You may assume that in all warehouse maps all boxes are
# reachable from beginning (robot is not boxed in).

# -------------------
# User Instructions
#
# Design a planner (any kind you like, so long as it works).
# This planner should be a function named plan() that takes
# as input three parameters: warehouse, dropzone and todo. 
# See parameter info below.
#
# Your function should RETURN the final, accumulated cost to do
# all tasks in the todo list in the given order and this cost
# must which should match with our answer).
# You may include print statements to show the optimum path,
# but that will have no effect on grading.
#
# Your solution must work for a variety of warehouse layouts and
# any length of todo list.
# 
# --------------------
# Parameter Info
#
# warehouse - a grid of values. where 0 means that the cell is passable,
# and a number between 1 and 99 shows where the boxes are.
# dropzone - determines robots start location and place to return boxes 
# todo - list of tasks, containing box numbers that have to be picked up
from math import sqrt

MOVES = [
    [-1, -1, 1.5], [-1,  0, 1.0], [-1,  1, 1.5],
    [ 0, -1, 1.0],                [ 0,  1, 1.0],
    [ 1, -1, 1.5], [ 1,  0, 1.0], [ 1,  1, 1.5],
]

class Map:
    def __init__(self, grid, gx, gy):
        self.gx, self.gy = gx, gy
        self.closed = [[0]*len(grid[0]) for _ in range(len(grid))]
        self.open = []
    
    def is_unexplored(self, x, y):
        return (self.closed[x][y] == 0)
    
    def heuristic(self, x, y):
        return sqrt((self.gx-x)**2 + (self.gy-y)**2)
    
    def add(self, cost, x, y):
        self.closed[x][y] = 1
        h = cost + self.heuristic(x, y)
        self.open.append([h, cost, x, y])
    
    def get_next(self):
        self.open.sort()
        _, cost, x, y = self.open.pop(0)
        return cost, x, y

class Warehouse:
    def __init__(self, warehouse, dropzone, todo):
        self.warehouse = warehouse
        self.dropzone = dropzone
        
        box_coordinates = {}
        for x in range(len(warehouse)):
            for y in range(len(warehouse[0])):
                n = warehouse[x][y]
                if n in ['x', 0]: continue
                else: box_coordinates[n] = [x, y]
        
        self.todo = [box_coordinates[n] for n in todo]
    
    def is_accessible(self, x, y):
        return (x >= 0 and x < len(self.warehouse)    and
                y >= 0 and y < len(self.warehouse[0]) and
                self.warehouse[x][y] == 0)
    
    def box_path_cost(self, bx, by):
        map = Map(self.warehouse, bx, by)
        map.add(0, self.dropzone[0], self.dropzone[1])
        
        while True:
            if len(map.open) == 0:
                raise Exception("No route from dropzone to box")
            
            cost, x, y = map.get_next()
            if x == bx and y == by:
                return cost
            
            for dx, dy, cm in MOVES:
                xm, ym = x+dx, y+dy
                if (self.is_accessible(xm, ym) and map.is_unexplored(xm, ym)):
                    map.add(cost+cm, xm, ym)
    
    def cost(self):
        c = 0
        for bx, by in self.todo:
            self.warehouse[bx][by] = 0
            c += self.box_path_cost(bx, by) * 2
        return c

def plan(warehouse, dropzone, todo):
    return Warehouse(warehouse, dropzone, todo).cost()

################# TESTING ##################
# ------------------------------------------
# solution check - Checks your plan function using
# data from list called test[].
def solution_check(test, epsilon = 0.00001):
    answer_list = []
    
    import time
    start = time.clock()
    correct_answers = 0
    for i in range(len(test[0])):
        user_cost = plan(test[0][i], test[1][i], test[2][i])
        true_cost = test[3][i]
        if abs(user_cost - true_cost) < epsilon:
            print "\nTest case", i+1, "passed!"
            answer_list.append(1)
            correct_answers += 1
            #print "#############################################"
        else:
            print "\nTest case ", i+1, "unsuccessful. Your answer ", user_cost, "was not within ", epsilon, "of ", true_cost 
            answer_list.append(0)
    runtime =  time.clock() - start
    if runtime > 1:
        print "Your code is too slow, try to optimize it! Running time was: ", runtime
        return False
    if correct_answers == len(answer_list):
        print "\nYou passed all test cases!"
        return True
    else:
        print "\nYou passed", correct_answers, "of", len(answer_list), "test cases. Try to get them all!"
        return False

#Testing environment
# Test Case 1 
warehouse1 = [[ 1, 2, 3],
             [ 0, 0, 0],
             [ 0, 0, 0]]
dropzone1 = [2, 0] 
todo1 = [2, 1]
true_cost1 = 9

# Test Case 2
warehouse2 = [[  1, 2, 3, 4],
             [   0, 0, 0, 0],
             [   5, 6, 7, 0],
             [ 'x', 0, 0, 8]] 
dropzone2 = [3, 0] 
todo2 = [2, 5, 1]
true_cost2 = 21

# Test Case 3
warehouse3 = [[  1, 2, 3, 4, 5, 6,  7],
             [   0, 0, 0, 0, 0, 0,  0],
             [   8, 9,10,11, 0, 0,  0],
             [ 'x', 0, 0, 0, 0, 0, 12]] 
dropzone3 = [3, 0] 
todo3 = [5, 10]
true_cost3 = 18

# Test Case 4
warehouse4 = [[  1,17, 5,18, 9,19, 13],
             [   2, 0, 6, 0,10, 0, 14],
             [   3, 0, 7, 0,11, 0, 15],
             [   4, 0, 8, 0,12, 0, 16],
             [   0, 0, 0, 0, 0, 0, 'x']] 
dropzone4 = [4, 6] 
todo4 = [13, 11, 6, 17]
true_cost4 = 41

testing_suite = [[warehouse1, warehouse2, warehouse3, warehouse4],
                 [dropzone1, dropzone2, dropzone3, dropzone4],
                 [todo1, todo2, todo3, todo4],
                 [true_cost1, true_cost2, true_cost3, true_cost4]]

solution_check(testing_suite)
