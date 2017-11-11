import math

cdef extern from "math.h":
    double cos(double theta)

def pr(double phi_pre, double gj=0.0, double w=1.9):
    cdef double dt = 0.00390625
    cdef double pi = math.pi
    cdef double p = pi 
    cdef double po = pi+dt
    cdef int reset = 0
    cdef int already_hit = 0
    cdef double t1=0.0, tf, dp
    cdef int cnt = 0
    cdef int i, steps

    
    steps = int(1000.0/dt)
    for i in range(steps):
        dp = w*cos(p) - 2.0
        po = p
        p += dt*dp
        if p < -pi: 
            p += 2*pi
            cnt += 1
        if cnt>5:
            break
        t1 = i*dt

    cdef double t2=t1
    steps = int(200.0/dt)
    for i in range(steps):
        if not already_hit:
            hit = po >= phi_pre and p < phi_pre
            already_hit = hit
        else:
            hit = 0
        dp = (w - gj*(1 if hit else 0)/dt)*cos(p) - 2
        po = p
        p += dt*dp
        t2 += dt
        if p < -pi: 
            break
    
    return t2-t1

# put in other necessary simulations as well


