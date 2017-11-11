# coding: utf-8
from pylab import *
from time import sleep

X,Y = mgrid[-pi:pi:100j, -pi:pi:100j]
V1 = sin(2*pi*X)*normpdf(1-X**2-Y**2, 0, 1)
V2 = cos(2*pi*Y)*normpdf(1-X**2-Y**2, 0, 1)

"""
figure()
subplot(131)
imshow(V1)
subplot(132)
imshow(V2)

subplot(133)
"""
q = lambda theta: V1*sin(2*pi*theta) + V2*cos(2*pi*theta)
img = imshow(q(0.0))

def animate_qspace():
	for i in mgrid[0:9:300j]:
		img.set_data(q(i))
		sleep(0.05)
		draw()
    
"""

this is kind of a cool little thing. I'd like to develop 
more this mode level thing. 
"""
