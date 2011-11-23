from MachineLearning.bayes import NaiveBayesClassifier, result


SPAM = (
    "offer is secret",
    "click secret link",
    "secret sports link",
)
HAM = (
    "play sports today",
    "went play sports",
    "secret sports event",
    "sports is today",
    "sports costs money",
)

print "=== Naive Bayes CLassifier ==="
c = NaiveBayesClassifier(SPAM, HAM)
print "Size of vocabulary: %d" % c.different_words
result("SPAM", c.spam.p, 0.3750)
result("secret|SPAM", c.spam.p_word("secret"), 0.3333)
result("secret|HAM",  c.ham.p_word("secret"), 0.0667)
result("SPAM|sports", c.p_spam_given_word("sports"), 0.1667)
result("SPAM|secret is secret)", c.p_spam_given_phrase("secret is secret"), 0.9615)
result("SPAM|today is secret)", c.p_spam_given_phrase("today is secret"), 0)

print "\n=== Naive Bayes CLassifier with Laplace Smoothing ==="
c = NaiveBayesClassifier(SPAM, HAM, 1)
result("SPAM", c.spam.p, 0.4)
result("HAM", c.ham.p, 0.6)
result("today|SPAM", c.spam.p_word("today"), 0.0476)
result("today|HAM",  c.ham.p_word("today"), 0.1111)
result("SPAM|today is secret)", c.p_spam_given_phrase("today is secret"), 0.4858)


from MachineLearning.linear_regression import linear_regression, gaussian
from scipy import matrix
print "\n=== Linear Regression ==="
x = [3,  4,  5,  6]
y = [0, -1, -2, -3]
(w0, w1), err = linear_regression(x, y)
print "(w0=%.1f, w1=%.1f) err=%.2f" % (w0, w1, err)

x = [2, 4, 6, 8]
y = [2, 5, 5, 8]
(w0, w1), err = linear_regression(x, y)
print "(w0=%.1f, w1=%.1f) err=%.2f" % (w0, w1, err)

x = matrix([[3],
            [4],
            [5],
            [6],
            [7]])
m, s = gaussian(x)
print "m  = %s" % str(m)
print "s^2= %s" % str(s)

x = matrix([[3],
            [9],
            [9],
            [3]])
m, s = gaussian(x)
print "m  = %s" % str(m)
print "s^2= %s" % str(s)

x = matrix([[3, 8],
            [4, 7],
            [5, 5],
            [6, 3],
            [7, 2]])
m, s = gaussian(x)
print "m  = %s" % str(m)
print "s^2= %s" % str(s)