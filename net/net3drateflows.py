from netsim import *

# show 2d projections of 3d phase flows
# 1. "cooperation"
# 2. winnerless competition / cycle
# 3. winner competition / multistability
# 4. monostability

# use mlab here or matplotlib? 
# I'd prefer 2d if possible

figure()

def makeg(g, mu=0, alpha=0):
    from numpy import array
    me = 0
    return array([[ me, g + (1-alpha)*mu, g - mu], [g - (1 - alpha)*mu, me, g + mu], [g + mu, g - mu, me]])

class proj2d:
    p = array([ [0.7, 0.0, -0.2 ], [0.1, .8, -0.2] ] )
    def __call__(self, ys)
        return dot(self.p, ys.T)

figure()
ax1 = plt.subplot2grid((3,2), (0, 0), rowspan=2)
ax2 = [plt.subplot2grid((3,2), (i, 1)) for i in range(3)]
G = makeg(-0.5)
plt.subplot2grid((3,2), (2, 0)).pcolor(G)
for i in range(3):
    s = Sim(3)
    s.G = G
    s.I = 0
    s.ds = int(1/s.dt)
    s.tw = 70.0
    ic = rand(3)*2
    print ic
    ic2d = proj2d(ic)
    ax1.plot(ic2d[0], ic2d[1], 'o')
    s.omega = ic
    s.ds = 20*int(1/s.dt)
    s.run(900)
    ys = proj2d()(s.ys[:,3:])
    ax1.plot(ys[0,:], ys[1,:], 'k', alpha=0.4)
    ys1 = proj2d()(s.rs)
    ax1.plot(ys1[0,:], ys1[1,:], 'k')
    ax2[i].plot(s.ys[:,3:],'k',alpha=0.6)
    ax2[i].plot(s.rs,'bgr'[i])

# fixed point
subplot(221)
grid(1)

# cycle
subplot(222)
grid(1)

# multistability
subplot(223)
grid(1)

# monostability
subplot(224)
grid(1)
