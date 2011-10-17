from collections import defaultdict
from copy import deepcopy
from heapq import heappush, heappop


def generate_state_space(data):
    """
    Generate our state space graph given a set of possible actions:
    data = [
        (state_a, state_b, cost),
        ...
    ]
    """
    state_space = defaultdict(list)
    for state_a, state_b, cost in data:
        state_space[state_a].append((state_b, cost))
        state_space[state_b].append((state_a, cost))
    return state_space


class GraphSearch:
    """
    The state_space is a graph where each node is a state and each edge is an
    action. Each action has a cost.
    A solution to a problem is a path between two states: the initial state and
    the goal state.
    
    state_space = {
        state_a: [
            (state_b, cost)
            ...
        ]
        state_b: [
            (state_a, cost)
            ...
        ]
        ...
    }
    action = (new_state, cost)
    path = ((state_1, state_2, ...state_n), cost, length)
    """
    def __init__(self, state_space):
        self.__state_space = state_space
    
    def actions(self, state):
        return self.__state_space[state]
    
    def step(self, path, action):
        new_path = deepcopy(path)
        new_path.add(action)
        return new_path
    
    def add_frontier(self, path):
        self.frontier[path.end] = path
        self.add_path(path)
    
    def add_path(self, path):
        self.paths.append(path)
    
    def already_in_frontier(self, new_path, adjacent):
        pass
    
    def search(self, initial_state, goal, heuristic=None, debug=False):
        self.heuristic = heuristic
        self.paths = []
        self.frontier = {}
        explored = set([])
        self.add_frontier(Path(initial_state))
        
        iterations = 0
        while True:
            iterations += 1
            path = self.get_path()
            if path is None: return None
            if debug: print path
            
            s = path.end
            explored.add(s)
            del self.frontier[s]
            if s == goal:
                return (path, iterations)
            
            for a in self.actions(s):
                new_node = a[0]
                if new_node in explored: continue
                
                new_path = self.step(path, a)
                if new_node in self.frontier:
                    self.already_in_frontier(new_path, new_node)
                else:
                    self.add_frontier(new_path)


class Path:
    def __init__(self, start):
        self.states = [start]
        self.cost = 0
        self.length = 0
    
    def add(self, action):
        self.states.append(action[0])
        self.cost += action[1]
        self.length += 1
    
    @property
    def end(self):
        return self.states[-1]
    
    def __str__(self):
        return ' -> '.join(self.states)  + " (cost:%d, length:%d)" % (self.cost, self.length)


class BreadthFirstSearch(GraphSearch):
    def get_path(self):
        return self.paths.pop(0)


class DepthFirstSearch(GraphSearch):
    def get_path(self):
        return self.paths.pop()


class UniformCostSearch(GraphSearch):
    def add_path(self, path):
        heappush(self.paths, (self.path_cost(path), path))
    
    def get_path(self):
        return heappop(self.paths)[1]
    
    def path_cost(self, path):
        return path.cost
    
    def already_in_frontier(self, new_path, adjacent):
        if self.path_cost(new_path) < self.path_cost(self.frontier[adjacent]):
            del self.frontier[adjacent]
            self.add_frontier(new_path)


class AStarSearch(UniformCostSearch):
    def path_cost(self, path):
        return path.cost + self.heuristic[path.end]

