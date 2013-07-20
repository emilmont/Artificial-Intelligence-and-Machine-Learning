#! /usr/bin/python
from __future__ import division
import sys, re, json
from collections import defaultdict

"""
Evaluate a set of test parses versus the gold set. 
"""

class ParseError(Exception):
  def __init__(self, value):
    self.value = value
    
  def __str__(self):
    return self.value


class TreeOperations:
  "Some basic operations on trees." 
  def __init__(self, tree): 
    self.tree = tree

  def _remove_vertical_markovization(self, nt):
    "Remove the vertical markovization." 
    return re.sub(r"\^<.*?>", '', nt)

  def _convert_to_spans(self, tree, start, set, parent = None): 
    "Convert a tree into spans (X, i, j) and add to a set." 
    if len(tree) == 3:
      # Binary rule.
      # Remove unary collapsing.
      current = self._remove_vertical_markovization(tree[0]).split("+")
      split = self._convert_to_spans(tree[1], start, set, None)
      end = self._convert_to_spans(tree[2], split + 1, set, current[-1])

      # Add phrases to set
      if current[0] != parent: 
        set.add((current[0], start, end))
      for nt in current[1:]:
        set.add((nt, start, end))
      return end
    elif len(tree) == 2:
      # Unary rule.
      
      # Can have a constituent if it is collapsed.
      current = self._remove_vertical_markovization(tree[0]).split("+")
      for nt in current[:-1]:
        set.add((nt, start, start))
      return start

  def to_spans(self):
    "Convert the tree to a set of nonterms and spans."
    s = set()
    self._convert_to_spans(self.tree, 1, s)
    return s

  def _fringe(self, node):
    if len(node) == 2: return [node[1]]
    else: return self._fringe(node[1]) + self._fringe(node[2])

  def fringe(self):
    "Return the fringe of the tree."
    return self._fringe(self.tree)

  def _well_formed(self, node):
    if len(node) not in [2, 3]:
      raise ParseError("Ill-formed tree:  %d-ary rule, only binary or unary allowed %s"%(len(node), node))
    
    if not isinstance(node[0], basestring):
      raise ParseError("Ill-formed tree: non-terminal not a string %s."%(node[0]))

    if len(node) == 2:
      if not isinstance(node[1], basestring):
        raise ParseError("Ill-formed tree: unary rule does not produce a string %s."%(node[1]))
    elif len(node) == 3:
      if isinstance(node[1], basestring):
        raise ParseError("Ill-formed tree: binary rule produces a string %s."%(node[1]))
      if isinstance(node[2], basestring):
        raise ParseError("Ill-formed tree: binary rule produces a string %s."%(node[2]))
      self._well_formed(node[1])
      self._well_formed(node[2])
      
  def check_well_formed(self):
    self._well_formed(self.tree)

class FScore:
  "Compute F1-Score based on gold set and test set."

  def __init__(self):
    self.gold = 0
    self.test = 0
    self.correct = 0

  def increment(self, gold_set, test_set):
    "Add examples from sets."
    self.gold += len(gold_set)
    self.test += len(test_set)
    self.correct += len(gold_set & test_set)

  def fscore(self): 
    pr = self.precision() + self.recall()
    if pr == 0: return 0.0
    return (2 * self.precision() * self.recall()) / pr

  def precision(self): 
    if self.test == 0: return 0.0
    return self.correct / self.test

  def recall(self): 
    if self.gold == 0: return 0.0
    return self.correct / self.gold    

  @staticmethod
  def output_header():
    "Output a scoring header."
    print "%10s  %10s  %10s  %10s   %10s"%(
      "Type", "Total", "Precision", "Recall", "F1-Score")
    print "==============================================================="

  def output_row(self, name):
    "Output a scoring row."
    print "%10s        %4d     %0.3f        %0.3f        %0.3f"%(
      name, self.gold, self.precision(), self.recall(), self.fscore())


class ParseEvaluator:
  def __init__(self):
    self.total_score = FScore()
    self.nt_score = defaultdict(FScore)
    
  def compute_fscore(self, key_trees, predicted_trees):
    for trees in zip(key_trees, predicted_trees):
      tops = map(TreeOperations, trees)
      tops[0].check_well_formed()
      tops[1].check_well_formed()
      f1, f2 = tops[0].fringe(), tops[1].fringe()

      if len(f1) != len(f2): 
        raise ParseError("Sentence length does not match. Gold sentence length %d, test sentence length %d. Sentence '%s'"%(len(f1), len(f2), " ".join(f1)))

      for gold, test in zip(f1, f2):
        if test != "_RARE_" and  gold != test:
          raise ParseError("Tree words do not match. Gold sentence '%s', test sentence '%s'."%(" ".join(f1), " ".join(f2)))
      set1, set2 = tops[0].to_spans(), tops[1].to_spans()

      # Compute non-terminal specific stats.
      for nt in set([s[0] for s in set1 | set2]):
        filter_s1 = set([s for s in set1 if s[0] == nt])
        filter_s2 = set([s for s in set2 if s[0] == nt])
        self.nt_score[nt].increment(filter_s1, filter_s2)

      # Compute total stats.
      self.total_score.increment(set1, set2)
    return self.total_score

  def output(self):
    "Print out the f-score table."
    FScore.output_header()
    nts = self.nt_score.keys()
    nts.sort()
    for nt in nts:
      self.nt_score[nt].output_row(nt)
    print
    self.total_score.output_row("total")

def main(key_file, prediction_file):
  key_trees = [json.loads(l) for l in key_file]
  predicted_trees = [json.loads(l) for l in prediction_file]
  evaluator = ParseEvaluator()
  evaluator.compute_fscore(key_trees, predicted_trees)
  evaluator.output()

if __name__ == "__main__": 
  if len(sys.argv) != 3:
    print >>sys.stderr, """
    Usage: python eval_parser.py [key_file] [output_file]
        Evalute the accuracy of a output trees compared to a key file.\n"""
    sys.exit(1)
  if sys.argv[1][-4:] != ".key":
    print >>sys.stderr, "First argument should end in '.key'."
    sys.exit(1)
  main(open(sys.argv[1]), open(sys.argv[2])) 


