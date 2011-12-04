print "\n=== Problem 2 ==="
from ProblemSolving.search import generate_state_space, AStarSearch

GRAPH = [
    ( "1",  "2", 10), ( "1",  "3", 10), ( "1",  "4", 10), ( "1",  "5", 10),
    ( "1",  "6", 10), ( "2",  "7", 10), ( "3",  "8", 10), ( "3",  "9", 10),
    ( "5", "10", 10), ( "5", "11", 10), ( "6", "12", 10), ("11", "12", 10),
]
HEURISTIC = {
     "1": 15, "2": 11,  "3": 8, "4": 7, "5": 6, "6": 10, "7": 2, "8": 3, "9": 9,
    "10": 5, "11": 20, "12": 0,
}
alg = AStarSearch(generate_state_space(GRAPH))
path, iterations = alg.search("1", "12", HEURISTIC, debug=True)
print "Found path in %d iterations: %s" % (iterations, path)

print "\n=== Problem 5 ==="
from BayesNetworks.bayes_net import BayesNetwork, P
COIN_NET = (
    ("F", 0.5),
    ("H1", (
        ({"F":True}, 0.5),
        ({"F":False}, 1.0)
    )),
    ("H2", (
        ({"F":True}, 0.5),
        ({"F":False}, 1.0)
    )),
)
n = BayesNetwork(COIN_NET)
P(n, {"F":False}, {"H1":True})
P(n, {"F":False}, {"H1":True, "H2":True})

print "\n=== Problem 7 ==="
TEST_NET = (
    ("A", 0.5),
    ("B", (
        ({"A":True}, 0.2),
        ({"A":False}, 0.2)
    )),
    ("C", (
        ({"A":True}, 0.8),
        ({"A":False}, 0.4)
    )),
)
n = BayesNetwork(TEST_NET)
P(n, {"B":True}, {"C":True})
P(n, {"C":True}, {"B":True})

print "\n=== Problem 8 ==="
from MachineLearning.bayes import NaiveBayesClassifier, result
SPAM = (
    "Top Gun",
    "Shy People",
    "Top Hat",
)
HAM = (
    "Top Gear",
    "Gun Shy",
)
c = NaiveBayesClassifier(SPAM, HAM, 1)
result("OLD", c.spam.p)
result("Top|OLD", c.spam.p_word("Top"))
result("OLD|Top", c.p_spam_given_word("Top"))


print "\n=== Problem 10 ==="
from MachineLearning.linear_regression import linear_regression, gaussian
x = [1.0, 3.0, 4.0, 5.0,  9.0]
y = [2.0, 5.2, 6.8, 8.4, 14.8]
(w0, w1), err = linear_regression(x, y)
print "(w0=%.1f, w1=%.1f) err=%.2f" % (w0, w1, err)


print "\n=== Problem 12 ==="
from Logic.logic import Proposition, implies
print Proposition(
    lambda a: not a,
             "not a"
).satisfiability_report()
print Proposition(
    lambda a: a or (not a),
             "a or (not a)"
).satisfiability_report()
print Proposition(
    lambda a, b, c: implies((a and (not a)), implies(b, c)),
                   "(a and (not a)) => (b => c)"
).satisfiability_report()
print Proposition(
    lambda a, b, c: implies(a, b) and implies(b, c) and implies(c, a),
                    "(a => b) and (b => c) and (c => a)"
).satisfiability_report()
print Proposition(
    lambda a, b, c: implies(a, b) and (not ((not a) or b)),
                    "(a => b) and (not ((not a) or b))"
).satisfiability_report()
print Proposition(
    lambda a, b, c: (implies(a, b) or implies(b, c)) == implies(a, c),
                    "((a => b) and (b => c)) == (a => c)"
).satisfiability_report()


print "\n=== Problem 14 ==="
from MDP.grid import GridWorld
GRID = [[0, 0, None, 100],
        [0, 0,    0,   0]]

PROB = {
    'S':(('S', 1.0), ),
    'N':(('N', 1.0), ),
    'E':(('E', 1.0), ),
    'W':(('W', 1.0), ),
}

STATES = ((1,3),(1,2),(1,1),(0,1),(1,0),(0,0))
g = GridWorld(GRID, PROB, STATES, 1, -5)
i = g.value_iteration(0.1)
print "Values after %d iterations:" % i
print g

print "\n=== Problem 15 ==="
from Markov.markov import TransProb
TRANSITIONS = [("A","A","A","A","B")]
t = TransProb(TRANSITIONS)
t.report(k=1)
