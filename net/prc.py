from numpy import *

import netsim

fn = lambda p,g,o: T(p,g,o)/T(0,0,o)-1
T = lambda p,g,o: 2*Q(o)*(A(p,o)-A(p+g*sin(p), o)-pi)
Q = lambda o: sqrt(1-o**2)/(o**2-1)
A = lambda p,o: arctan(Q(o)*(sin(p)+o*cos(p)+o)/(cos(p)+1))

# varphi is linear phase, phi & theta are nonlinear (with time)
nl2l = lambda p, o: Q(o)*(2*A(p,o)-pi)/T(0, 0, o)

def f(g, o):
    nl_p = r_[-pi:pi:100j]
    l_p = nl2l(nl_p, o)
    nlf = fn(nl_p, g, o)
    def prc(lp):
        return interp(lp, l_p, nlf)
    return prc

def fprime(g, o):
    _f = f(g, o)
    dp = 1./50
    lp = r_[0:1+1e-4:dp]
    df = diff(_f(lp))
    lp = lp[:-1]+dp/2.
    boundary = (df[0] + df[-1])/2
    def fp(p):
        return interp(p, lp, df, left=boundary, right=boundary)
    return fp

class dphi(object):
    def __init__(self, g, o, do=0.0):
        self.t1, self.t2 = T(0, 0, o-do), T(0, 0, o+do)
        self.f1, self.f2, = f(g, o-do), f(g, o+do)
    def __call__(self, p):
        t1, t2, f1, f2 = self.t1, self.t2, self.f1, self.f2 
        return (t2/t1)*(1+f2( (t1/t2)*(1 - p + f1(p)) )) - (1+f1(p))
    def diff(self, p):
        return diff(self(p))


