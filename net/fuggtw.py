# mean firing rate >> tau_w  approximation

from pylab import *

# using seconds, not milliseconds here

def sim(tf, tw, fu, dt=0.0001, ds=10, k=1):

    p_spike = lambda  : poisson(fu*dt)
    e_spike = lambda i: 1 if i%int(1/(fu*dt)) == 0 else 0

    wm, wp, we = 0., 0., 0.

    wms, wps, wes, ts = [], [], [], []

    for i in xrange(int(tf/dt)):

        wm += dt*(-wm + k*fu)/tw
        wp += dt*(-wp + k*p_spike( )/dt)/tw
        we += dt*(-we + k*e_spike(i)/dt)/tw

        if i%ds == 0:
            wms.append(wm)
            wps.append(wp)
            wes.append(we)
            ts.append(i*dt)

    return array(ts), array([wms, wps, wes]).T

def compare(tws=1./r_[3:40:20j], fu=20):

    def ssdiff(ys):
        return ((ys[:,0] - ys[:,1])**2).mean(), ((ys[:,0] - ys[:,2])**2).mean()

    def single(tw):
        return ssdiff(sim(1, tw, fu)[1])

    return tws, log(array(map(single, tws)))

def main():
    figure(figsize=(10, 8))

    subplot(221)
    plot(*sim(1, .144, 20))
    xlabel('time (s)')
    ylabel('$\\omega$')
    
    subplot(223)
    plot(*compare())
    xlabel('$\\tau_w$')
    ylabel('log(SSE)')

    subplot(222)
    plot(*sim(1, .144, 80))
    xlabel('time (s)')
    
    subplot(224)
    plot(*compare(fu=80))
    xlabel('$\\tau_w$')
    
    savefig('../doc/fig/fuggtw.png')
    
if __name__ == '__main__': main()