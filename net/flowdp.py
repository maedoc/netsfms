import math

ric = lambda : 2*pi*(rand()-0.5)
r, p = ric(), ric()
dt = 2**-4
mcos = math.cos
ts, rs, ps = [], [], []

for i in xrange(int(2**9/dt)):

    dr = (1.95 if i*dt>2**7 else 2.0)*mcos(r)/2 - 1
    r += dr*dt

    dp = (1.6 + (2 if r<-pi else 0))*mcos(p)/2 - 1
    p += dp*dt

    if r<-pi: r += 2*pi
    if p<-pi: p += 2*pi

    if i%(2/dt) == 0:
        ts.append(i*dt)
        rs.append(r)
        ps.append(p)

ts, rs, ps = map(array, [ts, rs, ps])
subplot(211); plot(ts, rs, ts, ps-pi); grid(1)
subplot(212); plot(ts, rs-ps); grid(1)
