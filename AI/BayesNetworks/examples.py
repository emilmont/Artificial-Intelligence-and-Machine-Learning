from BayesNetworks.bayes_net import BayesNetwork, P

print "\n=== Cancer Test ==="
CANCER_TEST = (
    ({"C":True}, 0.9),
    ({"C":False}, 0.2)
)
CANCER_NET = (
    ("C", 0.01),
    ("T1", CANCER_TEST),
    ("T2", CANCER_TEST),
)
n = BayesNetwork(CANCER_NET)
P(n, {"C":True}, {"T1":True})
P(n, {"C":True}, {"T1":True, "T2":True})
P(n, {"C":True}, {"T1":True, "T2":False})


print "\n=== Happiness ==="
HAPPY_NET = (
    ("S", 0.7),
    ("R", 0.01),
    ("H", (
        ({"S":True , "R":True }, 1.0),
        ({"S":False, "R":True }, 0.9),
        ({"S":True , "R":False}, 0.7),
        ({"S":False, "R":False}, 0.1),
    ))
)
n = BayesNetwork(HAPPY_NET)
P(n, {"R":True}, {"H":True, "S":True})
P(n, {"R":True}, {"H":True})
P(n, {"R":True}, {"H":True, "S":False})


print "\n=== Alarm ==="
ALARM_NET = (
    ("B", 0.001),
    ("E", 0.002),
    ("A", (
        ({"B":True , "E":True }, 0.95),
        ({"B":True , "E":False}, 0.94),
        ({"B":False, "E":True }, 0.29),
        ({"B":False, "E":False}, 0.001),
    )),
    ("J", (
        ({"A":True} , 0.90),
        ({"A":False}, 0.05)
    )),
    ("M", (
        ({"A":True }, 0.70),
        ({"A":False}, 0.01)
    )),
)
n = BayesNetwork(ALARM_NET)
P(n, {"J":True, "M":True, "A":True, "B":False, "E":False}, {})
P(n, {"B":True}, {"J":True, "M":True})


print "\n=== Wet Grass ==="
GRASS_NET = (
    ("C", 0.5),
    ("S", (
        ({"C":True} , 0.10),
        ({"C":False}, 0.50)
    )),
    ("R", (
        ({"C":True} , 0.80),
        ({"C":False}, 0.20)
    )),
    ("W", (
        ({"S":True , "R":True }, 0.99),
        ({"S":True , "R":False}, 0.90),
        ({"S":False, "R":True }, 0.90),
        ({"S":False, "R":False}, 0.00),
    )),
)
n = BayesNetwork(GRASS_NET)
P(n, {"C":True}, {})
P(n, {"S":True}, {"C":True})
P(n, {"R":True}, {"C":True})
P(n, {"W":True}, {"S":False, "R":True})
P(n, {"R":True}, {"S":True})
P(n, {"W":True}, {"C":True, "R":True, "S":False})


print "\n=== Traffic ==="
TRAFFIC_NET = (
    ("R", 0.1),
    ("T", (
        ({"R":True} , 0.8),
        ({"R":False}, 0.1)
    )),
    ("L", (
        ({"T":True} , 0.3),
        ({"T":False}, 0.1)
    )),
)
n = BayesNetwork(TRAFFIC_NET)
P(n, {"T":True}, {})
P(n, {"T":True, "L":True}, {})
P(n, {"T":True, "L":False}, {})
P(n, {"T":False, "L":True}, {})
P(n, {"T":False, "L":False}, {})
P(n, {"L":True}, {})
P(n, {"L":False}, {})
