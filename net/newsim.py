"""
theoretical results
-------------------

this paper: Movement dynamics in neural networks

definite:
- (lighthouse/spiking) nrl model w/ adaptation
- sfms in firing rate 2, 3 and modes networks
- connectivity matrices => hierarchitecture

nice to haves
- stdp in connections
- phase coordination sfms
- rate <--> phase coordinations
- existence of brain arch
- stability of brain arch in cog environment

application
-----------

autopoeitic modeling, stability of homeostatic 
brain architecture in a cognitive environment


"""

# challenge of homeostatic, normalized, stable 
# and dynamic responses

import math, random, numpy as np

def run(cos=math.cos, QQ=random.gauss):
    r, p, w = 0.0, 0.0, 0.0
    dt, w0, g = 2**-3, 3, +0.5
    ts, ps, ws, rs = [], [], [], []

    pcnt = 0
    for i in xrange(int(1000/dt)):
        dr = (2.4+cos(i*dt/70))*cos(r) - 2
        r += dr*dt
        dp = (1.9 + w - (1 if r<-pi else 0)/dt)*cos(p) - 2
        dw = -w/(10 if i*dt < 500 else 1)
        p += dp*dt
        if p<-pi:
            p += 2*pi
            dw += 1/dt
            pcnt += 1
        if r<-pi:
            r += 2*pi
        w += dw*dt/20
        if i % 100:
            ts.append(i*dt)
            ps.append(p)
            ws.append(w)
            rs.append(r)
    return np.array([ts, ps, ws, rs])

def pr(phi_pre, cos=math.cos):
    p, po = pi, pi
    dt = 2**-4
    reset = False
    ts, ps = [], []
    cnt = 0

    for i in xrange(int(1000/dt)):
        dp = 1.9*cos(p) - 2
        po = p
        p += dt*dp
        if p < -pi: 
            p += 2*pi
            cnt += 1
        if cnt>5:
            break
        ts.append(i*dt)
        ps.append(p)

    t0, tf = ts[-1], None
    for i in xrange(int(20/dt)):
        hit = po > phi_pre and p < phi_pre
        dp = (1.9 - 0.2*(1 if hit else 0)/dt)*cos(p) - 2
        po = p
        p += dt*dp
        ts.append(t0+i*dt)
        ps.append(p)
        if p < -pi: 
            tf = ts[-1]
            break
    
    return ts, ps, (tf-t0 if tf else None)

"""
ts, ps, ws, rs = run()

subplot(311); plot(ts, rs); grid(1)
subplot(312); plot(ts, ps); grid(1)
subplot(313); plot(ts, ws); grid(1)

print pcnt
"""

xs = r_[-pi:pi:500j]
cnts = [pr(p)[2] for p in xs]
plot(xs, cnts, xs, cos(xs)+10)


