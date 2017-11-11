from netsim import *


if False:
    n = 2
    s = Sim(n)
    s.tw = 30.0
    s.ds = 2/s.dt
    s.I = array([0.2, 0.21])
    #s.G[:,:] = 0.9/n
    sG = 0.9/n
    s.G = array([[sG, -sG], [sG, -sG]])
    s.run(1500)
    subplot(311)
    [plot(s.ts, s.ys[:,i], 'k', alpha=1.0/n) for i in range(n)]
    ylabel(r'$\phi_i(t)$')
    xticks([])

    subplot(312)
    Z = abs(exp(1j*s.ys[:,:n]).sum(axis=1)/n)
    plot(s.ts, Z, 'k', alpha=0.5)
    Zc = convolve(Z, ones(30)/30, 'valid')
    plot(arange(Zc.shape[0])*s.dt*s.ds, Zc, 'k')
    ylabel(r'$Z(\vec{\phi}(t))$')
    xticks([])
    ylim([0, 1.2])

    subplot(313)
    [plot(s.ts, s.ys[:,i+n], 'k', alpha=1./n) for i in range(n)]
    #[plot(s.rs[:,i]-1., 'k', alpha=1./n) for i in range(n)]
    xlabel('time')
    ylabel('$\omega_i(t)$')

# now multistability in relative phase!
n = 3
s = Sim(n)
s.tw = 30.0
s.ds = 5
s.I = 1.5 + randn(n)*0.05
s.G[:,:] = -1.5/n
s.run(500)
lim=2
js, ji = vstack(nonzero(dstack((s.ys[:-1,:n] < -lim, s.ys[1:,:n] > lim)).all(axis=2)))
subplot(311)
foo = lambda : [plot(s.ts, s.ys[:,i]+i*pi, 'k', alpha=1.0/sqrt(n)) for i in range(n)]
#[plot(s.ts, s.ys[:,i]+i*pi, 'k', alpha=1.0/n) for i in range(n)]
foo()
xlim([450, 500])
ylabel(r'$\phi_i(t)$')
xticks([])
grid(1)

subplot(312)
Z = abs(exp(1j*s.ys[:,:]).sum(axis=1)/n)
plot(s.ts, Z, 'k', alpha=0.5)
Zc = convolve(Z, ones(30)/30, 'valid')
plot(arange(Zc.shape[0])*s.dt*s.ds, Zc, 'k')
ylabel(r'$Z(\vec{\phi}(t))$')
xticks([])
ylim([0, 2])
grid(1)

subplot(313)
[plot(s.ts, s.ys[:,i+n], 'k', alpha=1./sqrt(n)) for i in range(n)]
plot(s.ts, (s.ys[:,n:]).sum(axis=1),'k')
#[plot(s.rs[:,i]-1., 'k', alpha=1./n) for i in range(n)]
xlabel('time')
ylabel('$\omega_i(t)$')
grid(1)

def diffs(js, ji, i, j):
    t1, t2 = js[ji==i], js[ji==j]
    n = min(t1.shape[0], t2.shape[0])
    return t1[:n] - t2[:n]

"""
figure()
plot(diffs(js, ji, 0, 1), 'x')
plot(diffs(js, ji, 0, 2), 'x')
plot(diffs(js, ji, 1, 2), 'x')
"""

def foosim(g=-1.5):
    s = Sim(n)
    s.tw = 30.0
    s.ds = 5
    s.I = 1.5 + randn(n)*0.05
    s.G[:,:] = g/n
    s.run(200)
    ps = d2cphase(s.ys[::1,:3])
    plot(ps[:,1]-ps[:,0], ps[:,2]-ps[:,0],'k', alpha=0.3)

figure()
ps = d2cphase(s.ys[::1,:3])
plot(ps[:,1]-ps[:,0], ps[:,2]-ps[:,0])
axis([-2*pi, 2*pi, -2*pi, 2*pi])
