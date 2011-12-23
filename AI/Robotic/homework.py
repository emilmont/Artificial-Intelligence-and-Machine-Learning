from math import pi
from motion import Position

p = Position(x=0, y=0, v=10, om=(pi/8.0), th=0, dt=4)
p.update(4)
print p
