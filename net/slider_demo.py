from pylab import *
import math
from matplotlib.widgets import Slider
from scipy.integrate import odeint 

def sqrt0(A):
    if hasattr(A, 'shape') and len(A.shape)>0:
        B = A.copy()
        B[A<0] = 0
        return sqrt(B)
    else:
        return 0.0 if A<0.0 else math.sqrt(A)

def dxy(y, t, ga, gaa, gx, gxa, I):
    X, Y = y
    DX = - X + sqrt0(4 - (ga*(1+gaa)*X+gx*(1+gxa)*Y+I)**2)
    DY = - Y + sqrt0(4 - (gx*(1-gxa)*X+ga*(1-gaa)*Y+I)**2)
    return array([DX, DY])

def compute(ga, gaa, gx, gxa, I, n=20j):
    X, Y = mgrid[-3:3.:n, -3:3:n]
    DX = - X + sqrt0(4 - (ga*(1+gaa)*X+gx*(1+gxa)*Y+I)**2)
    DY = - Y + sqrt0(4 - (gx*(1-gxa)*X+ga*(1-gaa)*Y+I)**2)
    return X, Y, DX, DY

fig = figure()
ax = subplot(111)
subplots_adjust(bottom=0.25)
x, y, dx, dy = compute(*[0.0]*5)
plotstuff = dict(
ncx = contour(x, y, dx, [-1, 0, 1]),
ncy = contour(x, y, dy, [-1, 0, 1]),
qvr = quiver(x, y, dx, dy))

def newslid(arg):
    pos, label, mn, mx, val = arg
    ax = axes([0.1, pos, 0.8, 0.02])
    return Slider(ax, label, mn, mx, valinit=val)

sga, sgaa, sgx, sgxa, sI = map(newslid, 
    [(0.01, 'ga', -6, 6, 0.), 
     (0.06, 'gaa', -3, 3, 0.),
     (0.11, 'gx', -6, 6, 0.),
     (0.16, 'gxa', -3, 3, 0.), 
     (0.21, 'I', -6, 6, 0.)])

def update(val):
    ga, gaa, gx, gxa, I = map(lambda x: x.val, [sga,sgaa, sgx,sgxa, sI])
    x, y, dx, dy = compute(ga, gaa, gx, gxa, I, n=60j)
    ax.clear()
    del plotstuff['ncx'], plotstuff['ncy'], plotstuff['qvr']
    plotstuff['ncx'] = ax.contour(x, y, dx, [-1, 0, 1])
    plotstuff['ncy'] = ax.contour(x, y, dy, [-1, 0, 1])
    plotstuff['qvr'] = ax.quiver(*compute(ga, gaa, gx, gxa, I))

map(lambda x: x.on_changed(update), [sga, sgaa, sgx, sgxa, sI])

def onclick(event):
    if not ax==event.inaxes:
        return None

    x, y = event.xdata, event.ydata
    print 'running sim with ic', x, y

    pars = map(lambda x: x.val, [sga,sgaa, sgx,sgxa, sI])
    ys = odeint(dxy, (x,y), r_[0:20:100j], args=tuple(pars))
    ax.plot(ys[:,0], ys[:,1], 'k', alpha=0.5)
    draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)

show()

