from Markov.markov import TransProb, MarkovChain, MarkovModel

print "\n=== Homework 6.1 ==="
OBSERVATIONS = (
    ("A", "B", "C", "A", "B", "C"),
    ("A", "A", "B", "B", "C", "C"),
    ("A", "A", "A", "C", "C", "C")
)
t = TransProb(OBSERVATIONS)
t.report()

print "\n=== Homework 6.2 ==="
CHAIN = ("A", 1.0, {True: 0.9, False: 0.5})
c = MarkovChain(CHAIN)
print "stationary distribution: P(A) = %.4f" % c.stationary_distribution(True)
print "stationary distribution: P(B) = %.4f" % c.stationary_distribution(False)

print "\n=== Homework 6.3 ==="
MODEL = ("A", 0.5, {True: 0.5, False: 0.5}, "X", {True: 0.1, False: 0.8})
m = MarkovModel(MODEL)
m.p({"A0":True}, {"X0":True})
m.p({"A1":True}, {"X0":True})
m.p({"A1":True}, {"X0":True, "X1":True})

print "\n=== Homework 6.11 ==="
from Game.game import Game
HW6_11 = {
    "players": (
        ("B", "d", "e", "f"),
        ("A", "a", "b", "c")
    ),
    "matrix": (
        ((3,3), (5,0), (2,1)),
        ((2,4), (7,8), (4,6)),
        ((7,5), (8,5), (5,3)),
    )
}
g = Game(HW6_11)
print "Dominant strategy for A: %s" % g.dominant_strategy("A")
print "Dominant strategy for B: %s" % g.dominant_strategy("B")
print "Equilibrium Points: %s" % str(g.equilibrium())
