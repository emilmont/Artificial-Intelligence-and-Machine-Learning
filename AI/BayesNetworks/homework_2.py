from BayesNetworks.bayes_net import BayesNetwork, P


print "\n=== Homework 2.1 ==="
HOMEWORK_1 = (
    ("A", 0.5),
    ("B", (
        ({"A":True}, 0.2),
        ({"A":False}, 0.8)
    )),
)
n = BayesNetwork(HOMEWORK_1)
P(n, {"A":True}, {"B":True})


TEST = (
    ({"A":True}, 0.2),
    ({"A":False}, 0.6)
)
HOMEWORK_2 = (
    ("A", 0.5),
    ("X1", TEST),
    ("X2", TEST),
    ("X3", TEST),
)
n = BayesNetwork(HOMEWORK_2)

print "\n=== Homework 2.2 ==="
P(n, {"A":True }, {"X1":True, "X2":True, "X3":False})

print "\n=== Homework 2.3 ==="
P(n, {"X3":True}, {"X1":True})