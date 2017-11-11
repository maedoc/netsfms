from pylab import *

def reset_plot():
    hold(0)
    plot(0)
    hold(1)

def excitator(a=0.0,b=0.0,tau=2.0):
    def excitator_inst(x,y):
        dx = (x + y - x**3/3)*tau
        dy =-(x - a + b*y)/tau
        return dx, dy
    return excitator_inst

def nullclines(sys, xl=2.0, yl=2.0):
    X, Y = mgrid[-xl:xl:50j, -yl:yl:50j]
    DX, DY = sys(X, Y)
    contour(X, Y, DX, [0], colors='r')
    contour(X, Y, DY, [0], colors='r')
    xticks([-1, 0, 1])
    yticks([-1, 0, 1])
    grid(1)

def sim(sys, xy0, tf=2**4, dt=2**-4):
    x, y = xy0
    ts, xs, ys = [0.0], [x], [y]

    for i in xrange(int(tf/dt)):
        dx, dy = sys(x, y)
        x += dt*dx
        y += dt*dy
        xs.append(x)
        ys.append(y)
        ts.append(i*dt)

    return array(ts), array(xs), array(ys)

pars = {'cy': {'a': 0.0 , 'b': 0.0},
        'mo': {'a': 1.3, 'b': 0.0},
        'bi': {'a': 0.0 , 'b': 2.0}}

excs = {kind: excitator(**par) for kind, par in pars.iteritems()}

xi = r_[ 0.5:2.0:10j]
yi = r_[-1.5:0.0:10j]

sims = {kind: [sim(sys,xy) for xy in zip(xi,yi)]
         for kind, sys in excs.iteritems()}

fig = figure()

# phase flows
subplot(231)
reset_plot()
nullclines(excs['bi'])
plot(xi, yi, 'k.')
[plot(xs, ys, 'k', alpha=0.5) for _, xs, ys in sims['bi']]
xlabel('x')
ylabel('y')

subplot(232)
reset_plot()
nullclines(excs['cy'])
plot(xi, yi, 'k.')
[plot(xs, ys, 'k', alpha=0.5) for _, xs, ys in sims['cy']]
xlabel('x')


subplot(233)
reset_plot()
nullclines(excs['mo'])
plot(xi, yi, 'k.')
[plot(xs, ys, 'k', alpha=0.5) for _, xs, ys in sims['mo']]
xlabel('x')


# time series?
subplot(234)
reset_plot()
[plot(ts, xs, 'k', alpha=0.4) for ts, xs, ys in sims['bi']]
yticks([-1, 0, 1])
xlabel('time')
ylabel('x')
grid(1)

subplot(235)
reset_plot()
[plot(ts, xs, 'k', alpha=0.4) for ts, xs, ys in sims['cy']]
yticks([-1, 0, 1])
xlabel('time')
grid(1)

subplot(236)
reset_plot()
[plot(ts, xs, 'k', alpha=0.4) for ts, xs, ys in sims['mo']]
yticks([-1, 0, 1])
xlabel('time')
grid(1)

savefig('fig/excitator-flows.png')

