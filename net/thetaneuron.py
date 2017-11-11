from pylab import *
import math as M

def reset():
    hold(0)
    plot(0)
    hold(1)

def flow(p, I):
    return I*cos(p)/2 - 1

def sim(p, I, tf=2**4, dt=2**-4):
    ts, ps = [0.0], [p]
    for i in xrange(int(tf/dt)):
        dp = I*M.cos(p)/2.0 - 1.0
        p += dt*dp
        if p < -pi:
            p += 2*pi
        ps.append(p)
        ts.append(i*dt)
    return ts, ps


P, I = mgrid[-pi:pi:50j, 0:4:50j]



fig = figure(figsize=(10,5))

dI = 0.3
Is = r_[0.0:3.1:dI] 
P, I = meshgrid(r_[-pi:pi:15j], Is)
cP, cI = mgrid[-pi:pi:50j, 0.0:3.1:50j]

# 1D phase flow
subplot(121)
reset()
DP = flow(P, I)
cDP = flow(cP, cI)
contour(cP, cI, cDP, [0.])
quiver(P, I, DP, 0., pivot='tail', minlength=2)
grid(1)
xlim((-pi, pi))
xticks([-pi, -pi/2, 0, pi/2, pi],
    ['$-\pi$', '$-\pi/2$', '$0$', '$\pi/2$', '$\pi$'])
yticks(Is)
ylim((Is[0]-2*dI, Is[-1]+2*dI))
xlabel('$\\theta$')
ylabel('I')

# time series
subplot(122)
reset()
for i, Ii in enumerate(Is):
    ts, ps = sim(pi, Ii)
    plot(ts, dI*array(ps)/(2.2*pi) + Ii, 'k')
grid(1)
yticks(Is,[])
xlabel('time')

savefig('fig/theta-neuron-flow-ts.png', dpi=300)

