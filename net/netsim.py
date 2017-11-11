"""
general network sims w/ reduction
"""

try:
    import cPickle as pickle
except ImportError:
    import pickle

import numpy as np
from pylab import *
from scipy import weave

def sqrt0(A):
    if hasattr(A, 'shape') and len(A.shape)>0:
        B = A.copy()
        B[A<0] = 0
        return sqrt(B)
    else:
        return 0.0 if A<0.0 else math.sqrt(A)


class Sim(object):

    def __init__(self, n):

        #import pdb; pdb.set_trace()

        # state
        self.t = 0
        self.theta = (rand(n)-0.5)*2*pi
        self.omega = rand(n)*2

        # parameters
        self.G = zeros((n, n))
        self.I = zeros(n)
        self.tw = 20.0

        self.dt = 2**-3
        self.ds = 1/self.dt

    def rvf(self, Omega):
        dp = dot(self.G, Omega.transpose([1, 0, 2]))
        return -Omega + sqrt0(4. - (dp + self.I)**2)

    def run(self, tf):

        n_steps = int(tf/self.dt)
        self.ts, self.ys, self.rs = [], [], []
        self.rmega = self.omega.copy()

        for i in xrange(n_steps):

            fired = self.theta < -pi
            self.theta[fired] += 2*pi

            dtheta = (dot(self.G, self.omega) + self.I)*cos(self.theta)/2. - 1.
            domega = -self.omega + 4*pi*fired.astype(int32)/self.dt

            drmega = -self.rmega + sqrt0(4. - 
                    (dot(self.G, self.rmega) + self.I)**2)

            self.theta += self.dt * dtheta
            self.omega += self.dt * domega/self.tw
            self.rmega += self.dt * drmega/self.tw
            self.t     += self.dt

            self.theta[self.theta>pi] = pi

            if i%self.ds==0:
                self.ts.append(self.t)
                self.ys.append(hstack((self.theta, self.omega)))
                self.rs.append(self.rmega.copy())

        self.ts = array(self.ts)
        self.ys = array(self.ys)
        self.rs = array(self.rs)


class Sim2(object):
    """
    Sim2 is identical to Sim except we're using sin not cos, 
    the 1/2 is disappeared into connectivty and input, which
    changes some of the fours and twos to ones.

    Since that change, the features of this class have expanded as well.
    """

    def _getI(self):
        if hasattr(self._I, '__call__'):
            return self._I(self.t)
        else:
            return self._I

    def _setI(self, val):
        self._I = val

    I = property(_getI, _setI)

    def set(self, **kwds):
        for key, value in kwds.iteritems():
            setattr(self, key, value)
        return self

    def dumps(self, simdtype=float32):
        """
        Store this simulation in a pickle-file with name 'fname'. Sim
        data if exists is downsampled to simdtype, to, by default, save
        space.

        """

        if hasattr(self, 'ys'):
            self.ts = self.ts.astype(simdtype)
            self.ys = self.ys.astype(simdtype)
            self.rs = self.rs.astype(simdtype)

        return pickle.dumps(self)

    def __hash__(self):
        string = "%r%r%r%r%r" % (self.G, self.I, self.tw,
                                 self.theta, self.omega)
        return hash(string)

    def zipwrite(self, zipfile):
        zipfile.writestr(str(hash(self)), self.dumps())

    @staticmethod
    def load(fname):
        """
        Load a simulation from a pickle-file

        """

        with open(fname, 'r') as fd:
            resurrected = pickle.load(fd)
        return resurrected

    def __init__(self, n, track_spikes=True):

        self.n = n
        self.indices = arange(n)

        # state
        self.t = 0
        self.theta = (rand(n)-0.5)*2*pi
        self.omega = rand(n)

        # parameters
        self.G = zeros((n, n))
        self.I = zeros(n)
        self.tw = 20.0

        self.dt = 2**-3
        self.ds = int(1/self.dt)

        # convenient spike tracking
        self.track_spikes = track_spikes
        if track_spikes:
            self.spike_times = [list() for _ in xrange(n)]

        self.rmega = self.omega.copy()
        self.ts = array([0.])
        self.ys = hstack((self.theta, self.omega))
        self.rs = self.rmega.copy()

    def rvf(self, Omega):
        dp = dot(self.G, Omega.transpose([1, 0, 2]))
        return -Omega + sqrt0(1. - (dp + self.I)**2)

    def run(self, tf, use_blitz=False):
        if use_blitz:
            self.cont1(tf)
        else:
            self.cont(tf)
        return self

    def cont1(self, dur=20, until=None):
        """
        A weave/blitz version of cont method, speedup for networks under 60 nodes.
        But the by-hand dot product makes this method slower for n>60 compared to pure
        numpy integration. Ideally, we'd make use of numpy.core._dotblas, but that
        doesn't seem very easy...

        We can get another 2x by using pointers to arrays directly, but the
        multidimensional access is nice.

        """

        n_steps = int(((until - self.t) if until else dur)/self.dt)
        nsave = n_steps/self.ds
        theta, omega, rmega, I, G, dt = self.theta, self.omega, self.rmega, self.I, self.G, self.dt
        n, t, ds, tw = self.n, self.t, self.ds, self.tw
        ts, ys, rs = zeros((nsave,)), zeros((nsave, 2*self.n)), zeros((nsave, self.n))
        code = """
        #line 131 "netsim.py"
        double dtheta, domega, drmega, coupling;
        int iout = 0;

        for (int i=0; i<n_steps; i++) {

            for (int j=0; j<n; j++) {

                domega = 0;

                if (theta(j)>pi) {
                    theta(j) -= 2*pi;
                    domega += 1; // this is not pi??
                }

                coupling = 0.0;
                for (int k=0; k<n; k++) coupling += G(j,k)*omega(k);

                dtheta = 1 + (coupling + I(j))*sin(theta(j));
                domega += -omega(j);
                drmega = -rmega(j);


                theta(j) += dt*dtheta;
                omega(j) += dt*domega/tw;
                rmega(j) += dt*drmega/tw;
                t += dt;
            }

            if (i%ds==0) {
                ts(iout) = t;
                for (int j=0; j<n; j++) {
                    ys(iout, j) = theta(j);
                    ys(iout, n+j) = omega(j);
                    rs(iout, j) = rmega(j);
                }
                //printf("ys(%d, 0) = %f\\n", iout, ys(iout,0));
                iout += 1;
            }
        }
        """
        passvars = ['n_steps', 'n', 'G', 'omega', 'theta', 'ts', 'ys', 'rs',\
                    'I', 'dt', 'pi', 'rmega', 't', 'ds', 'tw']
        weave.inline(code, passvars,
                type_converters=weave.converters.blitz, headers=['<math.h>', '<stdio.h>'],
                compiler='gcc',
                verbose=2)
        self.t = ts[-1]
        self.ts = hstack((self.ts, ts))
        self.ys = vstack((self.ys, ys))
        self.rs = vstack((self.rs, rs))

    def cont(self, dur=20, until=None):

        n_steps = int(((until - self.t) if until else dur)/self.dt)

        # accumulate data in lists
        ts, ys, rs = [], [], []

        for i in xrange(n_steps):

            fired = self.theta > pi
            # this allows reset thru spike
            self.theta[fired] -= 2*pi

            # if this is too slow, do in post-processsing
            if self.track_spikes:
                if fired.any():
                    for i in where(fired)[0]:
                        self.spike_times[i].append(self.t)

            dtheta = 1 + (dot(self.G, self.omega) + self.I)*sin(self.theta) 

            domega = -self.omega + pi*fired.astype(int32)/self.dt

            drmega = -self.rmega + sqrt0(1. - 
                    (dot(self.G, self.rmega) + self.I)**2)

            self.theta += self.dt*dtheta
            self.omega += self.dt*domega/self.tw
            self.rmega += self.dt*drmega/self.tw
            self.t     += self.dt

            self.theta[self.theta<-pi] = pi

            if i%self.ds==0:
                ts.append(self.t)
                ys.append(hstack((self.theta, self.omega)))
                rs.append(self.rmega.copy())


        # combine with previous or initial conditions
        self.ts = hstack((self.ts, array(ts))) # h not v cause its 1d
        self.ys = vstack((self.ys, array(ys)))
        self.rs = vstack((self.rs, array(rs)))

    ## all kinds of analyses we can add here

    @property
    def ratecov(self):
        return cov(self.ys[:,self.n:].T)


def d2cphase(ys, up=True, shift=2*pi, lim=2):
    if up:
        jump = dstack((ys[:-1] < -lim, ys[1:] > lim)).all(axis=2)
    else:
        jump = dstack((ys[:-1] > lim, ys[1:] < -lim)).all(axis=2)

    out = ys.copy()
    for i, j in zip(*nonzero(jump)):
        out[(i+1):, j] -= shift

    return out

def sumdiff(a,b=None):
    if b==None:
        a, b = a

    return a-b, a+b

