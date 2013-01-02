from math import sqrt, exp, pi


class Gaussian:
    def __init__(self, mu, sigma2):
        self.mu = float(mu)
        self.sigma2 = float(sigma2)
    
    def sense(self, measurement, sigma2):
        self.mu = (sigma2*self.mu + self.sigma2*measurement) / (self.sigma2 + sigma2)
        self.sigma2 = 1. / (1./self.sigma2 + 1./sigma2)
    
    def __str__(self):
        return "(mu:%.4f, sigma2:%.4f)" % (self.mu, self.sigma2)


if __name__ == '__main__':
    pos = Gaussian(1, 1)
    pos.sense(3, 1)
    print "Question 5: %s" % pos