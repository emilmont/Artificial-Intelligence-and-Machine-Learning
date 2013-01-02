R, G = 'red', 'green'

class Array:
    def __init__(self, n, init=0.):
        self.data = [init]*n
        self.n = n
    
    def sum(self):
        return sum(self.data)
    
    def __str__(self):
        return str(self.data)


class UniformArray(Array):
    def __init__(self, n):
        prob = (1. / float(n))
        Array.__init__(self, n, prob)


class HistogramFilter:
    def __init__(self, world, measurement_error):
        self.world = world
        self.p = UniformArray(len(world))
        
        self.pHit  = (1. - measurement_error)
        self.pMiss = measurement_error
    
    def sense(self, Z):
        # Add sensor information
        for i in range(self.p.n):
            self.p.data[i] *= (self.pHit if self.world[i] == Z else self.pMiss)
        
        # Normalise
        s = self.p.sum()
        for i in range(self.p.n):
            self.p.data[i] /= s
    
    def move(self, i_delta):
        q = Array(self.p.n)
        for i in range(self.p.n):
            i_move = i + i_delta
            if i_move < 0: i_move = 0
            elif i_move >= self.p.n: i_move = (self.p.n - 1)
            
            q.data[i_move] += self.p.data[i]
        
        self.p = q
    
    def __str__(self):
        return str(self.p)


if __name__ == '__main__':
    WORLD = [G, G, R, G, R]
    MEASUREMENT_ERROR = 0.1
    
    f = HistogramFilter(WORLD, MEASUREMENT_ERROR)
    f.sense(R)
    print "Question 3: %s" % f
    
    f.move(1)
    
    p_red   = f.p.data[2] + f.p.data[4]
    p_green = f.p.data[0] + f.p.data[1] + f.p.data[3]
    
    pHit  = (1. - MEASUREMENT_ERROR)
    pMiss = MEASUREMENT_ERROR
    
    p_red_m = (p_red*pHit) + (p_green*pMiss)
    
    print "Question 4: %.5f" % p_red_m
