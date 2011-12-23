from Logic.logic import Proposition, implies

def A(p, g): return p
def B(p, g): return (p or g)
def C(p, g): return (p and g)
def D(p, g): return implies((not p), g)

PROPOSITIONS = [A, B, C, D]
for p1 in PROPOSITIONS:
    for p2 in PROPOSITIONS:
        print Proposition(
            lambda p, g: implies(p1(p, g), p2(p, g)),
            "%s => %s" % (p1.__name__, p2.__name__)
        ).satisfiability_report()
