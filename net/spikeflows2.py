from pylab import *

import prc
from netsim import Sim2
from util import mapsubplot

mpl.rcParams['font.size'] = 16
fig = figure(figsize=(14,7))

fig.subplotpars.update(0.1, 0.07, 0.98, 0.98)

# mapsubplot(3,3,[1,2,3],title,[r'$f(\varphi)$', r'$\theta_i(t)$', r'$\|z(t)\|$'])
mapsubplot(3,3,[7,8,9],xlabel,[r'$\varphi$', 'time (ms)', 'time (ms)'])
mapsubplot(3,3,[1,4,7],ylabel,['fixed point', 'limit cycle', 'monostable'])

# dphi plots
p = r_[0:1:50j]
omega = 0.9
pars = [(0.005, 0.), (0.005, 0.005), (-0.028, 0.005)]

pert_start, pert_dur, pert_mag = [200, 500], [30, 30], [2, 3]
pert_end = [start + dur for start, dur in zip(pert_start, pert_dur)]
sim_end = 500.0

for i, par in enumerate(pars):
    g, do = par

    # we need to figure out the correct thing here
    subplot(3,3,3*i+1)
    plot(p, prc.f(g, omega+do)(p)/abs(g), 'k')
    plot(p, prc.f(g, omega-do)(p)/abs(g), 'k')
    grid(1)
    ylim([-1, 1])
    #yticks([-0.2, 0., 0.2])
    yticks([-1./2, 0, 1./2])
    #xticks([])

    #subplot(6,3,6*i+2)
    subplot(3,3,3*i+2)
    s = Sim2(2)
    s.ds=1
    s.tw = 1.
    s.theta = array([-2., 0.])
    s.I = array([omega + do, omega - do])
    s.G = array([[0. , g], [g, 0.]])
    if i is not 2:
        s.run(1000)
    else:
        # monostable case, need perturbation
        s.run(pert_start[0])

        # perturbation 1
        s.I = array([omega + pert_mag[0]*do, omega - pert_mag[0]*do])
        s.cont(pert_dur[0])
        s.I = array([omega + do, omega - do])

        s.cont(until=pert_start[1])

        # perturbation 2
        s.I = array([omega + pert_mag[1]*do, omega - pert_mag[1]*do])
        s.cont(pert_dur[1])
        s.I = array([omega + do, omega - do])

        # go to end
        s.cont(until=1000)

    [plot(s.ts, s.ys[:,j], 'k', alpha=0.5) for j in [0,1]]
    if i is 2:
        [plot([start, end], [-3.5, -3.5], 'r') for start, end in zip(pert_start, pert_end)]
    #yticks([-pi/2, 0, pi/2], [r'$-\pi/2$', r'$0$', r'$\pi/2$'])
    yticks([-pi, 0, pi], [r'$-\pi$', r'$0$', r'$\pi$'])
    ylim([-3*pi/2, 3*pi/2])
    tlo, thi = (0, 500) if i is not 2 else (200, 750)
    xticks([])
    xticks(r_[tlo:thi+0.001:100.0])
    xlim([tlo, thi])
    grid(1)

    subplot(3,3,3*i+3)
    Z = abs(exp(1j*s.ys[:,:2]).sum(axis=1)/2)
    #plot(s.ts, Z, 'k', alpha=0.5)
    convsize = 300
    Zc = convolve(Z, ones(convsize)/convsize, 'valid')
    plot((convsize + arange(Zc.shape[0]))*s.dt*s.ds, Zc, 'k', alpha=0.5)
    if i is 2:
        [plot([start, end], [1, 1], 'r') for start, end in zip(pert_start, pert_end)]

    nspikes = min(len(sts) for sts in s.spike_times)
    sts = array([s.spike_times[j][:nspikes] for j in [0, 1]]).T
    relsts =  (sts[:,0] - sts[:,1])/prc.T(0,0,omega) % 1.
    plot(sts[:,0], 0.5*relsts+0.5, 'k--')

    #yticks([0.5, 1.])
    yticks([])
    ylim([0.4, 1.1])
    xticks(r_[tlo:thi+101:200])
    grid(1)

savefig('fig/spike-flows2.png')
show()

