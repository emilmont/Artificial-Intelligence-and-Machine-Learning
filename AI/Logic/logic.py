from inspect import getargspec


def num_variables(p):
    return len(getargspec(p).args)


def table(n):
    assert (n >= 1)
    c = [[True], [False]]
    for _ in range(n-1):
        new_c = []
        for e in c:
            new_c.append(e+[True])
            new_c.append(e+[False])
        c = new_c
    return c


def implies(x, y):
    return (not x) or y


class Proposition:
    def __init__(self, p, description=None):
        self.p = p
        self.n = num_variables(p)
        self.description = description
        
        self.truth_table_values = []
        self.is_valid = True
        self.is_satisfiable = False
        for case in table(self.n):
            v = p(*case)
            if v:
                self.is_satisfiable = True
            else:
                self.is_valid = False
            self.truth_table_values.append(case + [v])
        
        self.is_unsatisfiable = not self.is_satisfiable
    
    ### Pretty Print ###
    
    TRUTH_LABEL = {True:"T", False:"F"}
    def truth_table(self):
        s = ["\n" if self.description is None else "\n### %s ###" % self.description]
        h = "| %s | p  |" % ' | '.join(["x%d" % i for i in range(self.n)])
        s.append(h)
        s.append('-' * len(h))
        for row in self.truth_table_values:
            s.append("| %s  |" % '  | '.join([Proposition.TRUTH_LABEL[v]
                                              for v in row]))
        return '\n'.join(s)
    
    def satisfiability_report(self):
        if self.is_valid:
            satisfiability = 'valid'
        elif self.is_satisfiable:
            satisfiability = 'satisfiable'
        else:
            satisfiability = 'unsatisfiable'
        d = "\n" if self.description is None else '\n"%s": ' % self.description
        return d + "is %s" % satisfiability
