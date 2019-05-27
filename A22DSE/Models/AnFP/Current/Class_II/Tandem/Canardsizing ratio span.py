# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:09:47 2019

@author: tomhu
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

MTOW = 20*10**3*9.81 #N
V = 0.72 * (1.4*287*(273.15-56.46))**0.5

CL = 0.7
rho = 0.0887
res= 100
l=50
cgpos = np.linspace(2,l-2,res)
cm0 = -0.16
k = 0.9
A1 = 20 #2.5 to 4.5
config = np.linspace(1,A1,res)
#c2lim = 3


cgpos, config = np.meshgrid(cgpos, config)
shape = cgpos.shape
cgpos = np.ravel(cgpos)
config = np.ravel(config)
#c1 = np.ravel(c1)
c1 = config
d1 = cgpos
d2 = l - cgpos
S = MTOW / (0.5*rho*V**2*CL)

ac = 0.1*180/math.pi#/((1-M**2)**0.5+0.1*180/math.pi/(math.pi*e1*np.ravel(Ac)))
aw = 0.1*180/math.pi#/((1-M**2)**0.5+0.1*180/math.pi/(math.pi*e1*np.ravel(Aw)))

a = -2*c1*d1-CL*d2+d1*CL
b = 2*c1*cm0+2*c1*S*d1-CL*S*d1+CL*d1
c = -c1*cm0*S-CL*S*d1

det = b**2-4*a*c

root1 = (-b+(det)**0.5)/(2*a)
root2 = (-b-(det)**0.5)/(2*a)
S2 = root2
S1 = S - S2
CL2 = (c1*cm0*S+CL*S*d1-CL*S2*d1)/(S2*d2-S2*d1+S*d1)
CL1 = CL-CL2
c1 = (S1/config)**0.5
#A2 = S2 / c2lim**2



c1 = c1.reshape(shape)
#A1  = A1.reshape(shape)
#A2 = A2.reshape(shape)
CL1 = CL1.reshape(shape)
CL2 = CL2.reshape(shape)
cgpos = cgpos.reshape(shape)
S1 = S1.reshape(shape)
S2 = S2.reshape(shape)
config = config.reshape(shape)
#fig = plt.figure(1)
#ax = fig.add_subplot(111, projection='3d')
#
#ax.plot_wireframe(cgpos, config,S1 )
#ax.plot_wireframe(cgpos,config,S2, color = 'r')
##plt.plot(cgpos,S1, 'k')
##plt.plot(cgpos, S2, 'b')
##plt.show()
#fig = plt.figure(2)
#ax = fig.add_subplot(111, projection='3d')
#
#ax.plot_wireframe(cgpos, config,CL1 )
#ax.plot_wireframe(cgpos,config,CL2, color = 'r')
#
#fig = plt.figure(3)
#ax = fig.add_subplot(111, projection='3d')
#
#ax.plot_wireframe(cgpos, config,c1 )
##ax.plot_wireframe(cgpos,config,A2, color = 'r')
b1 = 50
b2 = 60

A1 = np.linspace(7,17,res)
A2 = np.linspace(7,17,res)

A1, A2 = np.meshgrid(A1, A2)
shape = A1.shape
A1, A2 = np.ravel(A1), np.ravel(A2)
c1 = b1/A1
c2 = b2 / A2
cgpos = 35
d1 = cgpos
d2 = l-cgpos


a = -S*d1
b = (cm0*S*c1*2-cm0*c1*S+cm0*c2*S+2*CL*S*d1+CL*S*d1-S*d2)
c = (-cm0*S*c1*CL-CL**2*S*d1)

det = b**2-4*a*c

root1 = (-b+(det)**0.5)/(2*a)
root2 = (-b-(det)**0.5)/(2*a)

CL2 = root2
CL1 = CL - CL2
S2 = CL2 * S/(2*CL2-CL)
S1 = S - S2

CL1 = CL1.reshape(shape)
CL2 = CL2.reshape(shape)
S1 = S1.reshape(shape)
S2 = S2.reshape(shape)
A1 = A1.reshape(shape)
A2 = A2.reshape(shape)
#fig = plt.figure(1)
#ax = fig.add_subplot(111, projection='3d')
#
#ax.plot_wireframe(A1, A2 , S1 )
#ax.plot_wireframe(A1,A2, S2, color = 'r')
#
#
#fig = plt.figure(2)
#ax = fig.add_subplot(111, projection='3d')
#
#ax.plot_wireframe(A1, A2 , CL1 )
#ax.plot_wireframe(A1,A2, CL2, color = 'r')

delta = 0.1