from pylab import *

import prc
from netsim import Sim2


mpl.rcParams['font.size']=18

fig= figure(figsize=(14, 9))
gs = [0.1, 0., -0.1]
p = r_[0:1:50j]
o = 0.8
subplot(221)
prcs = [prc.f(g, o)(p) for g in gs]
[plot(p, pr, 'k') for pr in prcs]
[plot(p[:-1], diff(pr), 'k', alpha=0.5) for pr in prcs]
xlabel(r'$\varphi$')
ylabel(r'$f(\varphi)$')
xticks([0, 0.5, 1])

df = lambda g, o, p, dp: (prc.f(g,o)(p+dp) - prc.f(g,o)(p))/dp
g = r_[-0.15:0.15:50j]
d = array([df(gi, o, 0, 1e-3)-1 for gi in g])
subplot(223)
plot(g, d,'k')
[plot(gi, df(gi, o, 0, 1e-3)-1, 'k*') for gi in gs]
xlabel(r'$g$')
ylabel(r'$\lambda$')
yticks(array(gs)-1)
xticks(gs)
grid(1)


for i, gi in enumerate(gs):
    s = Sim2(10)
    s.tw = 1
    s.ds = 1
    s.G = gi*(ones((10, 10))-identity(10))/10
    s.I[:] = o
    s.run(200)
    Z = abs(exp(1j*s.ys[:,:10]).sum(axis=1)/10.)
    Zc = convolve(Z, ones(100)/100., 'valid')
    subplot(3,2,2*(i+1))
    plot((100+arange(Zc.shape[0]))*s.dt*s.ds, Zc, 'k')
    yticks([0., 0.5, 1.])
    ylim([-0.2, 1.2])
    grid(1)
    xticks(r_[0:200+1:50],[]) if i<2 else xlabel('time (ms)')

savefig('fig/phase-mode-stability.png')
show()
