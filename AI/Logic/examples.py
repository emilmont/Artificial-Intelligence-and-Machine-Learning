from Logic.logic import Proposition, implies


print "implies(True, True)   = %s" % implies(True, True)
print "implies(False, False) = %s" % implies(False, False)

a = lambda p, q: p and implies(p, q)
print Proposition(a, "p and (p => q)").truth_table()

b = lambda p, q: not ((not p) or (not q))
print Proposition(b, "not ((not p) or (not q))").truth_table()

print Proposition(
    lambda p, q: a(p, q) == b(p, q),
                "(p and (p => q)) <=> (not ((not p) or (not q)))"
).truth_table()

print Proposition(
    lambda p: p or (not p),
             "p or (not p)"
).satisfiability_report()

print Proposition(
    lambda p: p and (not p),
             "p and (not p)"
).satisfiability_report()

print Proposition(
    lambda p, q: p or q or (p == q),
                "p or q or (p <=> q)"
).satisfiability_report()

print Proposition(
    lambda p, q: implies(p, q) or implies(q, p),
                "(p => q) or (q => p)"
).satisfiability_report()

print Proposition(
    lambda f, p, d: implies((implies(f, p) or implies(d, p)), implies(f and d, p)),
                    "((f => p) or (d => p)) => ((f and d) => p)"
).satisfiability_report()

