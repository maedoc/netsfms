#!/usr/bin/python

"""
Here we verify that the 2D rate equations have a Taylor expansion somewhat
like that of the Excitator equations for limit cycle regime

"""

from pylab import *
import netsim; reload(netsim)
from netsim import *

print 'limit cycle'

# prep network
s = Sim(2)
gxa, gx, gaa, ga = 0.77, -3.3, -1.71, -0.28
gxa, gx, gaa, ga = 0.77, -3.3, -2.5, -0.34
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
s.I = 2.86
s.I = 3.06
s.omega[:] = 1.5
s.omega[0] = 0.2
s.omega[1] = 0.7
s.tw = 50.0
s.ds = int(1/s.dt)
s.run(900)
# plot
clf()
Omega = mgrid[0:2:40j, 0:2:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0])
contour(O1, O2, dO[1], [0])
Omega = mgrid[0:2:10j, 0:2:10j]
O1, O2 = Omega
dO = s.rvf(Omega)
quiver(O1, O2, dO[0], dO[1], color='b')
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
axis([0, 2, 0, 2])
grid()
show()


# eval vector field
clf()
Omega = mgrid[0:2:40j, 0:2:40j]
O1, O2 = Omega
gxa, gx, gaa, ga = 0.77, -3.3, -1.71, -0.28
G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
I = 2.86
dp = dot(G, Omega.transpose([1, 0, 2]))
dO = -Omega + sqrt0(4. - (dp + I)**2)
contourf(O1, O2, dO[0], [0])
contourf(O1, O2, dO[0])
#contour(O1, O2, dO[1], [0])


