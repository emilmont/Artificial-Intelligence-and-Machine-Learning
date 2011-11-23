from Logic.logic import Proposition, implies

print Proposition(
    lambda s, f: implies(s, f) == (s or (not f)),
                "(s => f) <=> (s or (not f))"
).satisfiability_report()

print Proposition(
    lambda s, f: implies(s, f) == implies(not s, not f),
                "(s => f) <=> ((not s) => (not f))"
).satisfiability_report()

print Proposition(
    lambda s, f: implies(s, f) == implies(not f, not s),
                "(s => f) <=> ((not f) => (not s))"
).satisfiability_report()

print Proposition(
    lambda b, d: b or d or implies(b, d),
                "b or d or (b => d)"
).satisfiability_report()

print Proposition(
    lambda b, d: (b and d) == (not ((not b) or (not d))),
                "b and d <=> not ((not b) or (not d))"
).satisfiability_report()
