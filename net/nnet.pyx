import numpy as np
cimport cython, numpy as np
np.import_array()
ctypedef np.double_t DTYPE_t

cdef extern from "math.h":
    double cos(double theta)

def run(n,m):
    x = np.random.normal(size=(n,))
    b = np.random.normal(size=(n,))
    g = np.random.normal(size=(n,n))
    for i in xrange(m):
        x += 0.001*(np.dot(g, x) - 5*b*x)
    return x

# 30x speed up 
@cython.boundscheck(False)
def run3(int n, int m):
    cdef unsigned int i,j,k
    cdef double temp
    cdef np.ndarray[DTYPE_t] x = np.random.normal(size=(n,))
    cdef np.ndarray[DTYPE_t] b = np.random.normal(size=(n,))
    cdef np.ndarray[DTYPE_t, ndim=2] g = np.random.normal(size=(n,n))
    for i in xrange(m):
        for j in xrange(n):
            temp = 0.
            for k in xrange(n):
                temp += g[j,k]*x[k]
            x[j] += 0.001*(temp - 5*b[j]*x[j])
    return x

@cython.boundscheck(False)
def pr(double phi_pre, double gj=0.0):
    cdef double dt = 2**-8
    cdef double p = np.pi 
    cdef double po = np.pi+dt
    cdef int reset = 0
    cdef int already_hit = 0
    cdef double t1=0.0, tf, dp
    cdef int cnt = 0
    cdef int i
    cdef double pi = np.pi
    
    for i in xrange(int(1000/dt)):
        dp = 1.9*cos(p) - 2.0
        po = p
        p += dt*dp
        if p < -pi: 
            p += 2*pi
            cnt += 1
        if cnt>5:
            break
        t1 = i*dt

    cdef double t2=t1
    for i in xrange(int(40/dt)):
        if not already_hit:
            hit = po >= phi_pre and p < phi_pre
            already_hit = hit
        else:
            hit = 0
        dp = (1.9 - gj*(1 if hit else 0)/dt)*cos(p) - 2
        po = p
        p += dt*dp
        t2 += dt
        if p < -pi: 
            break
    
    return t2-t1

"""
# real simulation
def network_run(unsigned int N, g=None, I=None, q=None, s=None,
                double tau_s=20.0, int nsteps=100, int ds=10, double dt=0.1,
                ys=None, ts=None, double qr=-np.pi/2,
                dot=np.dot, npcos=np.cos, double pi=np.pi,
                array=np.array, bign=None):

    cdef np.ndarray[DTYPE_t, ndim=2] g = g or np.zeros((N, N))
    cdef np.ndarray[DTYPE_t] I = I or np.zeros((N,))
    cdef np.ndarray[DTYPE_t] q = q or np.zeros((N,))
    cdef np.ndarray[DTYPE_t] s = s or np.zeros((N,))
    cdef np.ndarray[DTYPE_t] dq = np.zeros((N,))
    cdef np.ndarray[DTYPE_t] ds = np.zeros((N,))
    cdef np.ndarray[DTYPE_t, ndim=2] ys = ys or np.zeros((nsteps, 2*N))
    cdef np.ndarray[DTYPE_t] ts = ts or np.zeros((nsteps,))

    cdef bool bign = bign or (True if N>200 else False)

    cdef unsigned int step, i, j, k, outcount = 0
    cdef double temp
    
    for step in xrange(nsteps):

        if bign:
            
            C = dot(g, s) - I
        
            H = array(q, copy=True)
            H[H<qr] = 10.
            H[H>=qr] = 0.

            ds = (H - s)/tau_s
            dq = (npcos(q)*C - 2.)/2.

            s += dt*ds
            q += dt*dq

            q[ q < -pi ] += 2*pi
        
        else:

            for i in xrange(N):

                temp = 0.
                for j in xrange(N):
                    temp += g[i,j]*s[j]

                ds[i] = ((10. if q[i]<qr else 0.) - s[i])/tau_s
                dq[i] = (cos(q[i])*(temp - I[i]) - 2.)/2.

            for i in xrange(N):
                s[i] += dt*ds[i]
                q[i] += dt*dq[i]
                if q[i] < -pi:
                    q[i] += 2*pi
            
            

        if step % ds == 0:
            ys[outcount, 0::2] = q
            ys[outcount, 1::2] = s
            ts[outcount] = step*dt
            outcount += 1

    return ts, ys
    
"""
        
