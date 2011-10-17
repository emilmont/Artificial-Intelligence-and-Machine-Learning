from search import *

ROMANIA_ROAD_MAP = [
    ("Arad", "Sibiu", 140),
    ("Arad", "Zerind", 75),
    ("Arad", "Timisoara", 118),
    ("Sibiu", "Fagaras", 99),
    ("Sibiu", "Rimnicu Vilcea", 80),
    ("Rimnicu Vilcea", "Craiova", 146),
    ("Rimnicu Vilcea", "Pitesti", 97),
    ("Pitesti", "Bucharest", 101),
    ("Drobeta", "Craiova", 120),
    ("Zerind", "Oradea", 71),
    ("Oradea", "Sibiu", 151),
    ("Timisoara", "Lugoj", 111),
    ("Lugoj", "Mehadia", 70),
    ("Mehadia", "Drobeta", 75),
    ("Craiova", "Pitesti", 138),
    ("Fagaras", "Bucharest", 211),
    ("Bucharest", "Giurgiu", 90),
    ("Bucharest", "Urziceni", 85),
]

ROMANIA_DISTANCES_FROM_BUCHAREST = {
    "Arad": 336,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Lugoj": 244,
    "Mehadia": 241,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Zerind": 374,
}

if __name__ == '__main__':
    state_space = generate_state_space(ROMANIA_ROAD_MAP)
    
    for Algorithm, heuristic in [
            (BreadthFirstSearch, None),
            (DepthFirstSearch, None),
            (UniformCostSearch, None),
            (AStarSearch, ROMANIA_DISTANCES_FROM_BUCHAREST),
        ]:
        print "\n=== %s ===" % Algorithm.__name__
        alg = Algorithm(state_space)
        solution = alg.search("Arad", "Bucharest", heuristic)
        path, iterations = solution
        print "Found path in %d iterations: %s" % (iterations, path)
