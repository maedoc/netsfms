from netsim import *

figure()
# fixed point
subplot(231)
s = Sim(2)
gxa, gx, gaa, ga = 0., 1., 0., 1.
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
print 'fixed point'
print 'gxa, gx, gaa, ga = ', gxa, gx, gaa, ga 
print 's.G = ', s.G
s.I = 0.
s.omega[0] = 1.8
s.omega[1] = 0.7
s.tw = 50.0
s.ds = int(1/s.dt)
s.run(900)
Omega = mgrid[-0.2:2.2:40j, -0.2:2.2:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0])
contour(O1, O2, dO[1], [0])
Omega = mgrid[-0.2:2.2:10j, -0.2:2.2:10j]
O1, O2 = Omega
dO = s.rvf(Omega)
quiver(O1, O2, dO[0], dO[1], color='blue')
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
axis([-0.2, 2.2, -0.2, 2.2])
xticks([], []), yticks([], [])
   
subplot(232)
# limit cycle
s = Sim(2)
gxa, gx, gaa, ga = 0.77, -3.3, -1.71, -0.28
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
print 'limit cycle'
print 'gxa, gx, gaa, ga = ', gxa, gx, gaa, ga 
print 's.G = ', s.G
s.I = 2.86
s.omega[:] = 1.5
s.tw = 50.0
s.ds = int(1/s.dt)
s.run(900)
Omega = mgrid[-0.2:2.2:40j, -0.2:2.2:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0])
contour(O1, O2, dO[1], [0])
Omega = mgrid[-0.2:2.2:10j, -0.2:2.2:10j]
O1, O2 = Omega
dO = s.rvf(Omega)
quiver(O1, O2, dO[0], dO[1], color='b')
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
axis([-0.2, 2.2, -0.2, 2.2])
xticks([], []), yticks([], [])

subplot(233)
# cycle nullcline overlay
Omega = mgrid[-0.9:2.6:90j, +0.6:2.3:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0], colors='k')
contour(O1, O2, dO[1], [0], colors='k')
#axis([-0.2, 2.2, -0.2, 2.2])
xticks([], []), yticks([], [])
xb = 1.0
dO1 = ((O1-xb)**9/3 - (O1-xb)/10)/10 + (O2 - 0.9)
dO2 = -(O2-2) + 0.0 - (gx*(1-gxa)*(O1-0.9) + ga*(1-gaa)*(O2-2))**2/1.4
contour(O1, O2, dO1, [0], colors='r')
contour(O1, O2, dO2, [0], colors='r')

subplot(234)
# bistability
s = Sim(2)
gxa, gx, gaa, ga = 0., -1.41, 0.0, 0.
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
print 'bistability'
print 'gxa, gx, gaa, ga = ', gxa, gx, gaa, ga 
print 's.G = ', s.G
s.I = 0.74
s.omega[0] = 1.0
s.omega[1] = 0.5
s.tw = 50.0
s.ds = int(1/s.dt)
s.run(900)
Omega = mgrid[-0.2:2.2:40j, -0.2:2.2:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0])
contour(O1, O2, dO[1], [0])
Omega = mgrid[-0.2:2.2:10j, -0.2:2.2:10j]
O1, O2 = Omega
dO = s.rvf(Omega)
quiver(O1, O2, dO[0], dO[1], color='b')
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
s = Sim(2)
gxa, gx, gaa, ga = 0., -1.41, 0.0, 0.
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
s.I = 0.74
s.tw = 50.0
s.ds = int(1/s.dt)
s.omega[0] = 0.5
s.omega[1] = 1.0
s.run(900)
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
axis([-0.2, 2.2, -0.2, 2.2])
xticks([], []), yticks([], [])

subplot(235)
# monostability
s = Sim(2)
gxa, gx, gaa, ga = 0.77, -3.3, -2.5, -0.34
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
print 'monostability'
print 'gxa, gx, gaa, ga = ', gxa, gx, gaa, ga 
print 's.G = ', s.G
s.I = 3.06
s.omega[0] = 0.1
s.omega[1] = 1.4
s.tw = 50.0
s.ds = int(1/s.dt)
s.run(900)
Omega = mgrid[-0.2:2.2:40j, -0.2:2.2:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0])
contour(O1, O2, dO[1], [0])
Omega = mgrid[-0.2:2.2:10j, -0.2:2.2:10j]
O1, O2 = Omega
dO = s.rvf(Omega)
quiver(O1, O2, dO[0], dO[1], color='b')
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
s = Sim(2)
gxa, gx, gaa, ga = 0.77, -3.3, -2.5, -0.34
s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
s.I = 3.06
s.tw = 50.0
s.ds = int(1/s.dt)
s.omega[0] = 0.2
s.omega[1] = 1.1
s.run(900)
plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
plot(s.rs[:,0], s.rs[:,1], 'k')
axis([-0.2, 2.2, -0.2, 2.2])
xticks([], []), yticks([], [])

subplot(236)
# monostability nullcline overlay
Omega = mgrid[-0.9:2.6:90j, +0.6:2.3:40j]
O1, O2 = Omega
dO = s.rvf(Omega)
contour(O1, O2, dO[0], [0], colors='k')
contour(O1, O2, dO[1], [0], colors='k')
#axis([-0.2, 2.2, -0.2, 2.2])
xticks([], []), yticks([], [])
xb = 1.0
dO1 = ((O1-xb)**9/3 - (O1-xb)/10)/10 + (O2 - 0.9)
dO2 = -(O2-2) + 0.2 - (gx*(1-gxa)*O1 + ga*(1-gaa)*(O2-2))**2
contour(O1, O2, dO1, [0], colors='r')
contour(O1, O2, dO2, [0], colors='r')

tight_layout()
savefig('fig/net-2d-cycle.png')
show()


