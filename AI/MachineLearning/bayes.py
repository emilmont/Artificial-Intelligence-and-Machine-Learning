from collections import Counter


class Type:
    def __init__(self, vocabulary, p, k, different_words):
        self.vocabulary = vocabulary
        self.norm = float(sum(vocabulary.values()) + k*different_words)
        self.p = p
        self.k = k
    
    def p_word(self, word):
        return float(self.vocabulary[word] + self.k) / self.norm
    
    def p_phrase(self, phrase):
        p = 1.0
        for word in phrase.split():
            p *= self.p_word(word)
        return p


class NaiveBayesClassifier:
    """
    P(spam|word) = P(word|spam) * (P(spam)/P(word))
    """
    def __init__(self, spam_data, ham_data, k=0):
        c_spam, c_ham = Counter(), Counter()
        for c, data in [(c_spam, spam_data), (c_ham, ham_data)]:
            for phrase in data:
                for word in phrase.split():
                    c[word] += 1
        
        norm = float(len(spam_data) + len(ham_data) + k*2)
        self.different_words = len((c_spam + c_ham).keys())
        
        self.spam = Type(c_spam, float(len(spam_data) + k) / norm, k, self.different_words)
        self.ham = Type(c_ham, float(len(ham_data) + k) / norm, k, self.different_words)
    
    def p_spam_given_word(self, word):
        p_spam = self.spam.p_word(word) * self.spam.p
        p_ham  = self.ham.p_word(word)  * self.ham.p
        return p_spam / (p_spam + p_ham)

    def p_spam_given_phrase(self, phrase):
        p_spam = self.spam.p_phrase(phrase) * self.spam.p
        p_ham  = self.ham.p_phrase(phrase)  * self.ham.p
        return p_spam / (p_spam + p_ham)


def result(name, value, expected=None):
    print "P(%s) = %.4f" % (name, value)
    if expected is not None:
        if abs(value - expected) > 0.0001:
            raise Exception("Expected: %.4f" % expected)
