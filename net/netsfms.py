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
from numpy import pi, r_, mgrid, array

import pr # cython sim


def plot_prs(gj, n=20, dopl=True, w=1.9):
    t0s = []
    ps = r_[-pi:pi:n*1j]
    if dopl:
        figure()
        subplot(211)
    for i, p in enumerate(ps):
        t0 = pr.pr(p, gj=gj, w=w)
        t0s.append(t0)
        if dopl:
            plot(ts, array(ys) + i*pi, 'k', alpha=0.4)

    if dopl:
        subplot(212)
        plot(ps, t0s)
        subplot(211)
        xlim((40.0, 100.0))

    return ps, t0s


def pr_gj_surf(gl=pi,w=1.9):
    gjs = r_[-gl:gl:50j]
    P, G = mgrid[-pi:pi:50j, -gl:gl:50j]
    curves = array([plot_prs(x, n=50, dopl=False, w=w)[1] for x in gjs])
    t0 = pr.pr(0., gj=0.0, w=w)
    return G, P, curves



"""
ts, ps, ws, rs = run()

subplot(311); plot(ts, rs); grid(1)
subplot(312); plot(ts, ps); grid(1)
subplot(313); plot(ts, ws); grid(1)

print pcnt

xs = r_[-pi:pi:500j]
cnts = [pr(p)[2] for p in xs]
plot(xs, cnts, xs, cos(xs)+10)

"""

# TODO for all these parameter sweeps, it would be a lot nicer
# to have the integration work on the arrays
