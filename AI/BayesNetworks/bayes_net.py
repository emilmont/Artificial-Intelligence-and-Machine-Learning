from types import FloatType


class Event:
    def __init__(self, conditions, p):
        self.conditions = conditions
        self.p = p
    
    def check(self, given):
        for event, value in given.iteritems():
            if self.conditions[event] != value:
                return False
        return True
    
    def __str__(self):
        return "%s: %.4f" % (self.conditions, self.p)


class BayesNetwork:
    def __init__(self, net):
        self.events = [Event({}, 1.0)]
        for name, probabilities in net:
            new_events = []
            for e in self.events:
                if type(probabilities) is FloatType:
                    p_true = probabilities
                else:
                    for given, p in probabilities:
                        if e.check(given):
                            p_true = p
                
                et_conditions = dict(e.conditions)
                et_conditions[name] = True
                et_p = e.p * p_true
                new_events.append(Event(et_conditions, et_p))
                
                ef_conditions = dict(e.conditions)
                ef_conditions[name] = False
                ef_p = e.p * (1.0 - p_true)
                new_events.append(Event(ef_conditions, ef_p))
            self.events = new_events
    
    def P(self, event, given):
        p_true = 0.0
        p_false = 0.0
        for e in self.events:
            if e.check(given):
                if e.check(event):
                    p_true += e.p
                else:
                    p_false += e.p
        return p_true / (p_true + p_false)


# "pretty" print of probability queries
SYM = {True:"", False:"-"}
def describe(e):
    return ','.join([SYM[value]+name for name, value in e.iteritems()])

def P(n, event, given={}, expected=None):
    p = n.P(event, given)
    
    description = describe(event)
    if given:
        description += "|" + describe(given)
    
    print "P(%s) = %.4f" % (description, p)
    
    if expected is not None:
        if abs(p - expected) > 0.001:
            raise Exception("Error evaluating P(%s): %.4f != %.4f" % (description, p, expected))
