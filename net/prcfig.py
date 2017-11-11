from pylab import *

import prc
from netsim import Sim2

# prepare 

fig = figure()

subplot(211)
s = Sim2(3)
s.ds = 1
s.tw = 100
s.omega[:] = 0.
s.theta = array([-pi/2, -pi/2, -1.7])
s.I[:] = array([0.96, 0.96, 0.98])
s.G = array([[0., 0., 0.], [0., 0., 0.5], [0., 0., 0.]])
s.run(50)
[plot(s.ts, s.ys[:,i]+[0,0,-3*pi/2][i], 'k', alpha=[0.5, 1, 1][i]) for i in range(3)]
yticks([0, -3*pi/2], [r'$\theta_{post}(t)$', r'$\theta_{pre}(t)$'])
grid(1)
# xlabel('time (ms)')

# prc and derivative
nl_p = r_[-pi:pi:100j]

subplot(223)
o, g = 0.5, 0.5
l_p = prc.nl2l(nl_p, o)
nlf = prc.fn(nl_p, g, o)
plot(l_p, nlf,'k')
plot(l_p, -g*sin(2*pi*l_p-pi)/prc.T(0,0,o), 'k', alpha=0.5)
# plot((nl_p+pi)/(2.*pi), nlf,'k', alpha=0.5)
xlabel(r'$\varphi$')
ylabel(r'$f$')
ylim([-0.15, .15])
grid(1)
yts = yticks()

subplot(224)
o, g = 0.5, -0.5
l_p = prc.nl2l(nl_p, o)
nlf = prc.fn(nl_p, g, o)
plot(l_p, nlf,'k')
#plot(l_p, prc.f(g, o)(l_p)+0.005)
#plot((nl_p+pi)/(2.*pi), nlf,'k', alpha=0.5)
plot(l_p, -g*sin(2*pi*l_p-pi)/prc.T(0,0,o), 'k', alpha=0.5)
xlabel(r'$\varphi$')
yticks(yts[0], ['' for _ in yts[1]])
ylim([-0.15, .15])
grid(1)

savefig('fig/prcfig.png', dpi=300)
show()

