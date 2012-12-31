from math import sqrt, exp, pi


class Gaussian:
    def __init__(self, mu, sigma2):
        self.mu = float(mu)
        self.sigma2 = float(sigma2)
        
        self.k1 = 1./sqrt(2.*pi*self.sigma2)
        self.k2 = -0.5/self.sigma2
    
    def value(self, x):
        return self.k1 * exp(self.k2 * (x-self.mu)**2)
    
    def sense(self, measurement, sigma2):
        self.mu = (sigma2*self.mu + self.sigma2*measurement) / (self.sigma2 + sigma2)
        self.sigma2 = 1. / (1./self.sigma2 + 1./sigma2)
    
    def move(self, motion, sigma2):
        self.mu = self.mu + motion
        self.sigma2 = self.sigma2 + sigma2
    
    def __str__(self):
        return "(mu:%.4f, sigma2:%.4f)" % (self.mu, self.sigma2)


if __name__ == '__main__':
    measurements = [5., 6., 7., 9., 10.]
    motion = [1., 1., 2., 1., 1.]
    measurement_sig = 4.
    motion_sig = 2.
    mu = 0
    sig = 10000
    pos = Gaussian(mu, sig)
    for i in range(len(measurements)):
        pos.sense(measurements[i], measurement_sig)
        pos.move(motion[i], motion_sig)
    
    print pos