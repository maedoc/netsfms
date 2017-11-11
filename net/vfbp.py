# coding: utf-8

"""
vfbp.py is basic code to use backpropagation to train a network
for a basic monostable SFM.

"""

from pylab import *

from pybrain.structure import TanhLayer
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets import SupervisedDataSet

N = 10
print 'make network', N, 'neurons'
XYnet = buildNetwork(N, N, N, hiddenclass=TanhLayer)

print 'build Excitator vector field dataset'
def vf(x, mu=0.4):
    dx1 = mu*(x[0] - x[0]**3/3.0 + x[1])*2
    dx2 = mu*(1.05 - x[0])/2
    dxr = -x[2:]
    return hstack((dx1, dx2, dxr))

figure()
XYds = SupervisedDataSet(N, N)
for i in range(10):
    x = (rand(N) - 0.5)*4
    xs = [x.copy()]
    for j in range(500):
        dx = vf(x)
        XYds.addSample(x.copy(), dx.copy())
        x += 0.1*(dx + randn(N)*1.0)
        xs.append(x.copy())
    xs = array(xs)
    plot(xs[:,0], xs[:,1], 'k', alpha=0.1)


print 'using backprop to train on vector field'
XYtrainer = BackpropTrainer(XYnet, XYds)
i, err = 0, XYtrainer.train()
while err>0.001 and i<100:
    i, err = i+1, XYtrainer.train()
    if i%10==0: print i, err
print 'final error', err

# simulate
figure()
x, xs = (randn(N)-0.5)*4, []
for i in range(2000):
    x += 0.1*(XYnet.activate(x) + randn(N)*0.05)
    xs.append(x.copy())
for i in range(2000):
    x += 0.1*(XYnet.activate(x) + randn(N)*0.2)
    xs.append(x.copy())
for i in range(2000):
    x += 0.1*(XYnet.activate(x) + randn(N)*0.05)
    xs.append(x.copy())
plot(array(xs))
