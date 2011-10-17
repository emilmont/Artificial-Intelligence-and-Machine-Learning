from search import *

class BreadthFirstSearchLeftToRight(UniformCostSearch):
    def path_cost(self, path):
        return path.length * 100 + ord(path.end)

class DepthFirstSearchLeftToRight(UniformCostSearch):
    def path_cost(self, path):
        return 1.0 / float(path.length * 100 + (100 - ord(path.end)))

class BreadthFirstSearchRightToLeft(UniformCostSearch):
    def path_cost(self, path):
        return path.length * 100 + (100 - ord(path.end))

class DepthFirstSearchRightToLeft(UniformCostSearch):
    def path_cost(self, path):
        return 1.0 / float(path.length * 100 + ord(path.end))

def breadth_vs_depth(graph, start, goal):
    state_space = generate_state_space(graph)
    for Algorithm in [
            BreadthFirstSearchLeftToRight,
            DepthFirstSearchLeftToRight,
            BreadthFirstSearchRightToLeft,
            DepthFirstSearchRightToLeft,
        ]:
        alg = Algorithm(state_space)
        solution = alg.search(start, goal)
        path, iterations = solution
        print "%s: %d" % (Algorithm.__name__, iterations)


if __name__ == '__main__':
    print "\n=== Homework 1.4: Search Tree ==="
    GRAPH_1 = [
        ("A", "B", 1),
        ("A", "C", 1),
        ("A", "D", 1),
        ("B", "E", 1),
        ("B", "F", 1),
        ("C", "G", 1),
        ("C", "H", 1),
        ("D", "I", 1),
        ("D", "J", 1),
    ]
    breadth_vs_depth(GRAPH_1, "A", "F")
    
    print "\n=== Homework 1.5: Search Tree 2 ==="
    GRAPH_2 = GRAPH_1 + [
        ("G", "K", 1),
        ("G", "L", 1),
        ("H", "M", 1),
    ]
    breadth_vs_depth(GRAPH_2, "A", "M")
    
    print "\n=== Homework 1.6: Search Network ==="
    GRAPH_3 = [
        ("A", "B", 1), ("A", "C", 1),
        ("B", "D", 1), ("B", "E", 1),
        ("C", "E", 1), ("C", "F", 1),
        ("D", "G", 1), ("D", "H", 1),
        ("E", "H", 1), ("E", "I", 1),
        ("F", "I", 1), ("F", "J", 1),
        ("P", "N", 1), ("P", "O", 1),
        ("N", "K", 1), ("N", "L", 1),
        ("O", "L", 1), ("O", "M", 1),
        ("K", "G", 1), ("K", "H", 1),
        ("L", "H", 1), ("L", "I", 1),
        ("M", "I", 1), ("M", "J", 1),
    ]
    breadth_vs_depth(GRAPH_3, "A", "J")
    
    print "\n=== Homework 1.7: Astar ==="
    TABLE = []
    for x in range(1,7):
        for y in ["a", "b", "c", "d"]:
            next_x = x+1
            if next_x < 7:
                TABLE.append(("%c%d"%(y,x) ,"%c%d"%(y,x+1),1))
            next_y = ord(y)+1
            if next_y < ord("e"):
                TABLE.append(("%c%d"%(y,x) ,"%c%d"%(chr(next_y),x),1))
    HEURISTIC = {
        "a1":4, "a2":4, "a3":4, "a4":3, "a5":2, "a6":1,
        "b1":3, "b2":3, "b3":3, "b4":3, "b5":2, "b6":1,
        "c1":2, "c2":2, "c3":2, "c4":2, "c5":2, "c6":1,
        "d1":1, "d2":1, "d3":1, "d4":1, "d5":1, "d6":0,
    }
    state_space = generate_state_space(TABLE)
    alg = AStarSearch(state_space)
    solution = alg.search("a1", "d6", HEURISTIC, debug=True)
    path, iterations = solution
    print "Found path in %d iterations: %s" % (iterations, path)