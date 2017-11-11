from pylab import *

import prc

mpl.rcParams['font.size'] = 18
figure(figsize=(12, 5))
subplot(121)
p1, p2 = mgrid[0:1:30j, 0:1:30j]
omega, domega = 0.5, 0.05
o1, o2 = omega+domega, omega-domega
g = 0.5
f1, f2 = prc.f(g, o1), prc.f(g, o2)
t1, t2 = prc.T(0,0,o1), prc.T(0,0,o2)
Al, Ar = t1*(1 - p1 + f1(p1)), t2*p2
Bl, Br = t1*p1, t2*(1 - p2 + f2(p2))
Acs = contour(p1, p2, Al-Ar, [0], colors='k')
Bcs = contour(p1, p2, Bl-Br+1, [1], colors='k')
# Acs.collections[0].get_paths()[0].vertices contains the lines for contours
fp1, fp2 = prc.fprime(g, o1), prc.fprime(g, o2)
lam = (fp1(p1) - 1)*(fp2(p2) - 1)
limit = min(abs(lam.min()), abs(lam.max()))
contour(p1, p2, abs(lam)-1, colors='k', alpha=0.5)
xlabel(r'$\varphi_1$')
ylabel(r'$\varphi_2$')

A = Acs.collections[0].get_paths()[0].vertices
B = Bcs.collections[0].get_paths()[0].vertices

def find_intersections(A, B):

    amin = lambda x1, x2: where(x1<x2, x1, x2)
    amax = lambda x1, x2: where(x1>x2, x1, x2)
    aall = lambda abools: dstack(abools).all(axis=2)
    slope = lambda line: (lambda d: d[:,1]/d[:,0])(diff(line, axis=0))

    x11, x21 = meshgrid(A[:-1, 0], B[:-1, 0])
    x12, x22 = meshgrid(A[1:, 0], B[1:, 0])
    y11, y21 = meshgrid(A[:-1, 1], B[:-1, 1])
    y12, y22 = meshgrid(A[1:, 1], B[1:, 1])

    m1, m2 = meshgrid(slope(A), slope(B))
    m1inv, m2inv = 1/m1, 1/m2

    yi = (m1*(x21-x11-m2inv*y21) + y11)/(1 - m1*m2inv)
    xi = (yi - y21)*m2inv + x21

    xconds = (amin(x11, x12) < xi, xi <= amax(x11, x12), 
              amin(x21, x22) < xi, xi <= amax(x21, x22) )
    yconds = (amin(y11, y12) < yi, yi <= amax(y11, y12),
              amin(y21, y22) < yi, yi <= amax(y21, y22) )

    return array([ xi[aall(xconds)], yi[aall(yconds)] ])

def exstab(g, o, do):
    p1, p2 = mgrid[0:1:30j, 0:1:30j]
    o1, o2 = o+do, o-do
    f1, f2 = prc.f(g, o1), prc.f(g, o2)
    t1, t2 = prc.T(0,0,o1), prc.T(0,0,o2)
    Al, Ar = t1*(1 - p1 + f1(p1)), t2*p2
    Bl, Br = t1*p1, t2*(1 - p2 + f2(p2))
    Acs = contour(p1, p2, Al-Ar, [0])
    Bcs = contour(p1, p2, Bl-Br+1, [1])
    fp1, fp2 = prc.fprime(g, o1), prc.fprime(g, o2)
    lam = lambda p1, p2: (fp1(p1) - 1)*(fp2(p2) - 1)
    A = Acs.collections[0].get_paths()
    B = Bcs.collections[0].get_paths()
    if len(A) and len(B):
        x, y = find_intersections(A[0].vertices, B[0].vertices)
        if len(x) is not len(y):
            print 'unequal x y intersect vector lenghts', x, y
            minl = min(len(x), len(y))
            x, y = x[:minl], y[:minl]
        return vstack((x, y, lam(x, y))).T
    else:
        return None
    
# asymmetry - connectivity plot
subplot(122)
if 0:
    ndo, ng = 50, 50
    dos, gs = meshgrid(linspace(0., 2e-2, ndo), linspace(-0.5, 0.5, ng))
    solx = nan*ones((ndo, ng))
    soly, soll = solx.copy(), solx.copy()

    for ii in xrange(ndo):
        for jj in xrange(ng):
            sol = exstab(gs[ii,jj], 0.9, dos[ii,jj])
            sol_stab = sol[abs(sol[:,2])<1,:] if isinstance(sol, ndarray) and sol.shape[0] else None
            if sol_stab is not None and sol_stab.shape[0]:
                solx[ii,jj], soly[ii,jj], soll[ii,jj] = sol_stab[0]


    hold(0)
    contourf(dos, gs, soll, cmap=cm.gray)

xlabel(r'$\|\omega_1 - \omega_2\|$')
ylabel(r'$g$')

#savefig('fig/prcexstab.png')
show()
