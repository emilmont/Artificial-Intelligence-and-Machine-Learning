from Markov.markov import MarkovChain, TransProb, MarkovModel

print "\nWeather Example"
WEATHER_CHAIN = ("R", 1.0, {True: 0.6, False: 0.2})
c = MarkovChain(WEATHER_CHAIN, 3)
c.p({"R1":True})
c.p({"R2":True})
c.p({"R3":True})
print "stationary distribution: P(R) = %.4f" % c.stationary_distribution()

print "\nA Example"
A_CHAIN = ("A", 1.0, {True: 0.5, False: 1.0})
c = MarkovChain(A_CHAIN, 3)
c.p({"A1":True})
c.p({"A2":True})
c.p({"A3":True})
print "stationary distribution: P(A) = %.4f" % c.stationary_distribution()

print "\nTransition Probabilities 1"
TRANSITIONS = [("R","S","S","S","R","S","R")]
t = TransProb(TRANSITIONS)
t.report()

print "\nTransition Probabilities 2"
TRANSITIONS = [("S","S","S","S","S","R","S","S","S","R","R")]
t = TransProb(TRANSITIONS)
t.report()

print "\nTransition Probabilities 3"
TRANSITIONS = [("R","S","S","S","S")]
t = TransProb(TRANSITIONS)
t.report(k=1)

print "\nMarkov Model 1"
MODEL = ("R", 0.5, {True: 0.6, False: 0.2}, "H", {True: 0.4, False: 0.9})
m = MarkovModel(MODEL)
m.p({"R1":True})
m.p({"R1":True}, {"H1":True})

print "\nMarkov Model 2"
MODEL = ("R", 1.0, {True: 0.6, False: 0.2}, "H", {True: 0.4, False: 0.9})
m = MarkovModel(MODEL)
m.p({"R1":True}, {"H1":True})
