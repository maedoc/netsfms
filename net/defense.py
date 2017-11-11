"""
Figures for the defense..

"""

if 0:
    import sys
    here = "c:/users/duke/desktop/thesis/netsfms/netsfms/net"
    if here not in sys.path:
        sys.path.append(here)

    import matplotlib as mpl
    mpl.use('Agg')    
    from pylab import *
    from numpy import *
    from netsim import Sim, Sim2

if 0:
    # just show spiking..
    n = Sim2(5)
    n.I[:] = 0.99
    n.G[:] = -0.01
    n.tw = 50.0
    n.dt = 0.1
    n.run(500)
    clf()
    for i, y, yl in zip([1, 2],
                        [n.ys[:, :n.n], n.ys[:, n.n:]],
                        [r'$\theta$', r'$\omega$']):
        subplot(2, 1, i)
        plot(n.ts/n.dt, y, 'k', alpha=0.5)
        grid(True)
        ylabel(yl)
        if i==1:
            xticks(xticks()[0], [])
        else:
            xlabel('time (steps)')
            
    savefig('c:/users/duke/desktop/thesis/gfx/netdemo.png', dpi=75)

if 1:

    close('all')
    mpl.rc('font', size=30)
    figure()
    subplot(111, frameon=True)
    s = Sim(2)
    gxa, gx, gaa, ga = 0.77, -3.3, -1.71, -0.28
    s.G = array([[ga*(1+gaa), gx*(1+gxa)], [gx*(1-gxa), ga*(1-gaa)]])
    print 'limit cycle'
    print 'gxa, gx, gaa, ga = ', gxa, gx, gaa, ga 
    print 's.G = ', s.G
    s.I = 2.86
    s.omega[:] = 1.5
    s.tw = 50.0
    s.ds = int(1/s.dt)
    s.run(900)
    Omega = mgrid[-0.2:2.2:40j, -0.2:2.2:40j]
    O1, O2 = Omega
    dO = s.rvf(Omega)
    contour(O1, O2, dO[0], [0])
    contour(O1, O2, dO[1], [0])
    Omega = mgrid[-0.2:2.2:10j, -0.2:2.2:10j]
    O1, O2 = Omega
    dO = s.rvf(Omega)
    quiver(O1, O2, dO[0], dO[1], color='b')
    plot(s.ys[:,2], s.ys[:,3], 'k', alpha=0.5)
    #plot(s.rs[:,0], s.rs[:,1], 'k')
    axis([-0.2, 2.2, -0.2, 2.2])
    xticks([]), yticks([])
    xlabel('$\\omega_1$')
    ylabel('$\\omega_2$')
    savefig('c:/users/duke/desktop/thesis/gfx/net2d_full.png', dpi=75)
