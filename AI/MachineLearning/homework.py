from MachineLearning.bayes import NaiveBayesClassifier, result

MOVIE = (
    "a perfect world",
    "my perfect woman",
    "pretty woman"
)
SONG = (
    "a perfect day",
    "electric storm",
    "another rainy day"
)
c = NaiveBayesClassifier(MOVIE, SONG, 1)
print "Size of vocabulary: %d" % c.different_words

print "\n=== Homework 3.1 ==="
result("MOVIE", c.spam.p)
result("SONG", c.ham.p)
result("perfect|MOVIE", c.spam.p_word("perfect"))
result("perfect|SONG",  c.ham.p_word("perfect"))
result("storm|MOVIE", c.spam.p_word("storm"))
result("storm|SONG",  c.ham.p_word("storm"))

print "\n=== Homework 3.2 ==="
result("MOVIE|perfect storm)", c.p_spam_given_phrase("perfect storm"))

print "\n=== Homework 3.3 ==="
c = NaiveBayesClassifier(MOVIE, SONG)
result("MOVIE|perfect storm)", c.p_spam_given_phrase("perfect storm"))

print "\n=== Homework 3.4 ==="
from MachineLearning.linear_regression import linear_regression
x = [0, 1, 2, 3,  4]
y = [3, 6, 7, 8, 11]
(w0, w1), err = linear_regression(x, y)
print "(w0=%.1f, w1=%.1f) err=%.2f" % (w0, w1, err)
