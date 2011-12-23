from math import sin, cos, pi

class Position:
    def __init__(self, x, y, th, v, om, t=0, dt=1):
        self.x = float(x)
        self.y = float(y)
        self.th = float(th)
        self.v = float(v)
        self.om = float(om)
        self.dt = float(dt)
    
    def update(self, steps=1):
        for _ in range(steps):
            d = self.v * self.dt
            self.x += d * cos(self.th)
            self.y += d * sin(self.th)
            self.th += self.om * self.dt
            if self.th >= 2*pi:
                self.th -= 2*pi
    
    def __str__(self):
        return '\n'.join([
             "x : %.2f" % self.x,
             "y : %.2f" % self.y,
             "th: %.2f" % self.th,
         ])
