# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 11:43:50 2019

@author: tomhu
"""
import numpy as np
import matplotlib.pyplot as plt
import math as m
#from mpl_toolkits.mplot3d import Axes3D

import os
from pathlib import Path
os.chdir(Path(__file__).parents[5])

#from A22DSE.Parameters.Par_Class_Diff_Configs import Conv

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

SFC = 26.25  * 10**-6 #kg/s/N
MThrust = 80*10**3 #N

n_engines = 6

W = 65000*9.81 #N

S = 400
CD0 = 0.01
CL = 0.7*0.86
A = 13
e = 0.75

"""Minimum time climb"""
#Max RC

res = 500
res1 = 50
z=res*res/res1
H = np.linspace(0,22000,res)
V = np.linspace(0,275,res)
V, H =  np.meshgrid(V,H)
shape = H.shape
MaxT = np.ones(shape)
rho = getatm(np.ravel(H))[1]
for i in range(len(MaxT[0])):
    MaxT[i,:] = MThrust * rho[res*i]/rho[0]


He = np.ravel(H) + np.power(np.ravel(V),2)/2/9.81


RCs = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)*S*\
       (CD0+CL**2/m.pi/A/e))*np.ravel(V)/W
       
RCs = RCs.reshape(shape)  
He = He.reshape(shape)
H = H.reshape(shape)
V = V.reshape(shape)     



tclimb=np.zeros((res))

He_ar = np.linspace(2000,22162.895,res1)
RCs_tmin = np.zeros(res1)
V_tmin = np.zeros(res1)
H_tmin = np.zeros(res1)
for i in range(len(He_ar)):
    RCs_tmin[i] = np.amax(RCs[np.where(np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))])
    index=(int(np.where(RCs == np.amax(RCs[np.where(\
        np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))]))[0]),\
    int(np.where(RCs == np.amax(RCs[np.where(\
        np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))]))[1]))
#    print(index)
    V_tmin[i] = V[index]
    H_tmin[i] = H[index]
    
#compute mdot/RCs

#He_opt = np.linspace(2000,22162.895,res1)
#RCs_opt = np.zeros(res1)
#V_opt = np.zeros(res1)
#H_opt = np.zeros(res1)
#for i in range(len(He_opt)):
#    RCs_opt[i] = np.amax(RCs[np.where(np.logical_and(He_opt[i]> He-z/res , He_opt[i] < He+z/res))])
#    index=(int(np.where(RCs == np.amax(RCs[np.where(\
#        np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))]))[0]),\
#    int(np.where(RCs == np.amax(RCs[np.where(\
#        np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))]))[1]))
##    print(index)
#    V_tmin[i] = V[index]
#    H_tmin[i] = H[index]       
       
#integrate         
       
       
       
       
       
       
       
       
#dRCdV = dRCdV.reshape(shape)



rho = rho.reshape(shape)
#invRCs = np.divide(1,RCs)



plt.figure(1)
a = plt.contour(np.power(V,2)/2/9.81,H,He,5,colors='k', linewidths = 0.5)
b = plt.contour(np.power(V,2)/2/9.81,H,RCs,20,colors='k')
plt.plot(np.power(V_tmin,2)/2/9.81,H_tmin)
plt.plot(206**2/2/9.81,20000,'k o')
plt.plot(np.ones(res)*129**2/2/9.81,H[:,0])
plt.clabel(b, inline=1, fontsize=10)
plt.show()


#plt.figure(2)
#a = plt.plot(He_ar, np.divide(1,RCs_tmin))
#plt.title('Climb time ='+ str(float(np.trapz(np.divide(1,RCs_tmin),He_ar))/60)+'min')
#plt.show()