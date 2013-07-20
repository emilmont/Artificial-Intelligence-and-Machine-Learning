from __future__ import division
from collections import Counter, defaultdict
from json import loads

from eval_parser import ParseEvaluator


def argmax(lst):
    return max(lst) if lst else (0.0, None)


class PCFG:
    def __init__(self, treebank):
        self.nonterminals = Counter()
        self.unary_rules = Counter()
        self.binary_rules = Counter()
        self.words = Counter()
        
        for s in open(treebank):
            self.count(loads(s))
        self.N = self.nonterminals.keys()
        
        # Set up binary rule table
        self.rules = defaultdict(list)
        for (sym, y1, y2) in self.binary_rules.keys():
            self.rules[sym].append((y1, y2))
        
        # Normalise the unary rules
        norm = Counter()
        for (sym, word), count in self.unary_rules.iteritems():
            norm[(sym, self.norm_word(word))] += count
        self.unary_rules = norm
    
    def count(self, tree):
        if isinstance(tree, basestring): return
        
        # Count the non-terminal symbols
        sym = tree[0]
        self.nonterminals[sym] += 1
        
        if len(tree) == 3:
            # Binary Rule
            y1, y2 = (tree[1][0], tree[2][0])
            self.binary_rules[(sym, y1, y2)] += 1
            
            # Recursively count the children
            self.count(tree[1])
            self.count(tree[2])
        
        elif len(tree) == 2:
            # Unary Rule
            word = tree[1]
            self.unary_rules[(sym, word)] += 1
            self.words[word] += 1
    
    def norm_word(self, word):
        return '_RARE_' if self.words[word] < 5 else word
    
    def q1(self, x, y):
        return self.unary_rules[(x, y)] / self.nonterminals[x]
    
    def q2(self, x, y1, y2):
        return self.binary_rules[(x, y1, y2)] / self.nonterminals[x]
    
    @staticmethod
    def backtrace(back, bp):
        # Extract the tree from the backpointers
        if not back: return None
        if len(back) == 6:
            (X, Y, Z, i, s, j) = back
            return [X, PCFG.backtrace(bp[i  , s, Y], bp),
                       PCFG.backtrace(bp[s+1, j, Z], bp)]
        else:
            (X, Y, i, i) = back
            return [X, Y]
    
    def CKY(self, sentence):
        x, n = [""] + sentence, len(sentence)
        
        # Charts
        pi = defaultdict(float)
        bp = {}
        for i in range(1, n+1):
            for X in self.N:
                if (X, x[i]) in self.unary_rules:
                    pi[i, i, X] = self.q1(X, x[i])
                    bp[i, i, X] = (X, x[i], i, i)
        
        # Dynamic program
        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i+l
                for X in self.N:
                    # Note that we only check rules that exist in training
                    # and have non-zero probability
                    score, back = argmax([(
                            self.q2(X, Y, Z) * pi[i, s, Y] * pi[s+1, j, Z],
                            (X, Y, Z, i, s, j)
                        ) for s in range(i, j)
                            for Y, Z in self.rules[X]
                                if pi[i  , s, Y] > 0.0
                                if pi[s+1, j, Z] > 0.0
                    ])
                    
                    if score > 0.0:
                        bp[i, j, X], pi[i, j, X] = back, score
        
        return PCFG.backtrace(bp[1, n, "SBARQ"], bp)
    
    def parse(self, sentence):
        return self.CKY(map(self.norm_word, sentence.strip().split()))


def test(pcfg, dat_path, key_path):
    evaluator = ParseEvaluator()
    evaluator.compute_fscore(
        [loads(tree) for tree in open(key_path)],
        [pcfg.parse(sentence) for sentence in open(dat_path)])
    evaluator.output()


if __name__ == "__main__":
    test(PCFG("parse_train.dat"), "parse_dev.dat", "parse_dev.key")
    test(PCFG("parse_train_vert.dat"), "parse_dev.dat", "parse_dev.key")
