"""
For defense
"""
from pylab import *
import prc
from netsim import Sim2
from util import mapsubplot

fig.subplotpars.update(0.1, 0.07, 0.98, 0.98)

# dphi plots
p = r_[0:1:50j]
omega = 0.9
pars = [(0, 0.005, 0.), (1, 0.005, 0.005), (2, -0.028, 0.005)]

pert_start, pert_dur, pert_mag = [200, 500], [30, 30], [2, 3]
pert_end = [start + dur for start, dur in zip(pert_start, pert_dur)]
sim_end = 500.0

figure(figsize=(10, 5))
for i, g, do in pars:
    clf()
    subplot(2, 1, 1)
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

    yticks([-pi, 0, pi], [r'$-\pi$', r'$0$', r'$\pi$'])
    ylim([-3*pi/2, 3*pi/2])
    tlo, thi = (0, 500) if i is not 2 else (200, 750)
    grid(1)
    xlim([0, 800])
    xticks(xticks()[0], [])

    subplot(2, 1, 2)
    Z = abs(exp(1j*s.ys[:,:2]).sum(axis=1)/2)
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
    #xticks(r_[tlo:thi+101:200])
    xlim([0, 800])
    grid(1)
    xlabel('Time')

    savefig('fig/spike-flows3-%d.png'%(i,))
