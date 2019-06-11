# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:43:50 2019

@author: tomhu
"""
import numpy as np
import matplotlib.pyplot as plt
import math as m
from mpl_toolkits.mplot3d import Axes3D

import os
from pathlib import Path
os.chdir(Path(__file__).parents[5])

from A22DSE.Parameters.Par_Class_Diff_Configs import Conv

def getatm(h):
    T = np.zeros(h.shape)
    p = np.zeros(h.shape)
    rho = np.zeros(h.shape)
    for i in range(len(h)) :
        if h[i] < 11000:
            T[i] = 15.04 - 0.00649 * h[i]
            p[i] = 101.29 * ((T[i]+273.1)/288.08)**5.256
        if h[i] >=11000 and h[i] <= 25000:
            T[i] = -56.46
            p[i] = 22.65*m.exp(1.73-0.000157*h[i])
    rho = np.multiply(p ,1/(0.2869*(T+273.1)))
    return T, rho, p

SFC = 22 #g/s/kN

 #kN

n_engines = 6

"""Minimum time climb"""
#Max RC

res = 100
H = np.linspace(0,22000,res)
V = np.linspace(0,275,res)
V, H =  np.meshgrid(V,H)
shape = H.shape
MaxT = np.ones(shape)
rho = getatm(np.ravel(H))[1]
for i in range(len(MaxT[0])):
    MaxT[i,:] = 80*10**3 * rho[100*i]/rho[0]


He = np.ravel(H) + np.power(np.ravel(V),2)/2/9.81
W = 60000*9.81 #N

S = 400
CD0 = 0.01
CL = 0.7
A = 13
e = 0.75

RCs = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)*S*\
       (CD0+CL**2/m.pi/A/e))*np.ravel(V)/W
       
       
#compute 1/RCs

       
#compute mdot/RCs

       
       
#integrate         
       
       
       
       
       
       
       
       

He = He.reshape(shape)
RCs = RCs.reshape(shape)
H = H.reshape(shape)
V = V.reshape(shape)
rho = rho.reshape(shape)
a = plt.contour(np.power(V,2)/2/9.81,H,He,5,colors='k', linewidths = 0.5)
b = plt.contour(np.power(V,2)/2/9.81,H,RCs,20,colors='k')
plt.plot(2162.9,20000,'k o')
plt.clabel(b, inline=1, fontsize=10)
plt.show()

