from collections import defaultdict, Counter

from BayesNetworks.bayes_net import BayesNetwork, P


class MarkovChain:
    def __init__(self, data, n_transitions=1):
        name, p0, self.p_trans = data
        
        e = "%s%%d" % name
        NET = [(e % 0, p0)]
        for i in range(n_transitions):
            NET.append((e % (i+1), (
                ({e % i:True }, self.p_trans[True]),
                ({e % i:False}, self.p_trans[False])
            )))
        
        self.net = BayesNetwork(NET)
    
    def p(self, event, given={}):
        P(self.net, event, given)
    
    def stationary_distribution(self, value=True):
        t = self.p_trans[False] / (1 - self.p_trans[True] + self.p_trans[False])
        if value:
            return t
        else:
            return (1 - t)


class TransProb:
    def __init__(self, observations):
        self.trans = defaultdict(list)
        self.states = set([])
        self.states_0 = Counter()
        self.obs_num = len(observations)
        for transitions in observations:
            self.states |= set(transitions)
            s0 = transitions[0]
            self.states_0[s0] += 1
            previous_state = s0
            for i in range(1, len(transitions)):
                new_state = transitions[i]
                self.trans[previous_state].append(new_state)
                previous_state = new_state
    
    def report(self, k=0):
        smoothing_norm = len(self.states) * k
        for s in self.states:
            p0 = float(self.states_0[s] + k) / float(self.obs_num + smoothing_norm)
            print "P(%s0) = %.4f" % (s, p0)
            for g in self.states:
                print "P(%s|%s) =" % (s, g),
                t = self.trans[g]
                if len(t) == 0 and k == 0:
                    print "Undefined"
                else:
                    p = float(t.count(s) + k) / float(len(t) + smoothing_norm)
                    print "%.4f" % p


class MarkovModel:
    def __init__(self, model, n_transitions=2):
        hidden_name, p0, p_trans, measure_name, p_measure = model
        
        h = "%s%%d" % hidden_name
        m = "%s%%d" % measure_name
        
        NET = [(h % 0, p0)]
        for i in range(n_transitions):
            NET.append((m % i, (
                ({h % i:True }, p_measure[True]),
                ({h % i:False}, p_measure[False])
            )))
            NET.append((h % (i+1), (
                ({h % i:True }, p_trans[True]),
                ({h % i:False}, p_trans[False])
            )))
        
        self.net = BayesNetwork(NET)
    
    def p(self, event, given={}):
        P(self.net, event, given)
