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

from A22DSE.Parameters.Par_Class_Conventional import Conv
from A22DSE.Parameters.Par_Class_Atmos import Atmos

anfp = Conv.ParAnFP
struc = Conv.ParStruc
prop = Conv.ParProp

ISA_model = Atmos()

def Lowbypass(Aircraft, Fsl, ISA_model, H):
    Tamb, Pamb = ISA_model.ISAFunc([H])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4)
    TR = 1.0
    if theta0 <= TR:
        F = 0.6*Fsl*delta0 #Empirical formula "General Aviation Aircraft Design, Applied Methods and Procedures" page 200
    else:
        F = 0.6*Fsl*delta0*(1-3.8*(theta0-TR)/(theta0))
    return F


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
MThrust = 60*10**3 #N

n_engines = prop.N_engines

W = struc.MTOW * 9.81

S = anfp.S
CD0 = anfp.CD0

A = anfp.A
e = anfp.e
CL = m.sqrt(CD0*m.pi*A*e)
"""Minimum time climb"""
#Max RC

res = 500
res1 = 100
z=res*res/res1
H = np.linspace(0,22000,res)
V = np.linspace(0,275,res)
V, H =  np.meshgrid(V,H)
shape = H.shape
MaxT = np.ones(shape)
rho = getatm(np.ravel(H))[1]
setting = np.linspace(0.2,1,res)
Thrust = np.ones(res)
for i in range(len(H)):
    Thrust[i] = Lowbypass(Conv, MThrust, ISA_model, H[i])
for i in range(len(MaxT[0])):
#    MaxT[i,:] = MThrust * rho[res*i]/rho[0]
    MaxT[i,:] = Thrust


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
thrust_tmin = np.zeros(res1)
for i in range(len(He_ar)):
    RCs_tmin[i] = np.amax(RCs[np.where(np.logical_and(He_ar[i]> He-z/res \
                          , He_ar[i] < He+z/res))])
    index=(int(np.where(RCs == np.amax(RCs[np.where(\
        np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))]))[0]),\
    int(np.where(RCs == np.amax(RCs[np.where(\
        np.logical_and(He_ar[i]> He-z/res , He_ar[i] < He+z/res))]))[1]))
    
    thrust_tmin[i] = MaxT[index]
    V_tmin[i] = V[index]
    H_tmin[i] = H[index]
    
#compute mdot/RCs

     
       
#integrate         
       
       
       
       
       
       
       
tmin = float(np.trapz(np.divide(1,RCs_tmin),He_ar))/60
fuel = float(np.trapz(np.divide(thrust_tmin,RCs_tmin),He_ar))*SFC*n_engines





plt.figure(1)
a = plt.contour(np.power(V,2)/2/9.81,H,He,5,colors='k', linewidths = 0.5)
b = plt.contour(np.power(V,2)/2/9.81,H,RCs,20,colors='k')
plt.plot(np.power(V_tmin,2)/2/9.81,H_tmin)
plt.plot(206**2/2/9.81,20000,'k o')
plt.plot(np.ones(res)*129**2/2/9.81,H[:,0])
plt.clabel(b, inline=1, fontsize=10)
plt.show()


plt.figure(2)
a = plt.plot(He_ar, np.divide(1,RCs_tmin))
plt.title('Climb time ='+ str(float(np.trapz(np.divide(1,RCs_tmin),He_ar))\
                              /60)+'min')
plt.show()


W = struc.MTOW * 0.95 * 9.81
RCs = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)*S*\
       (CD0+CL**2/m.pi/A/e))*np.ravel(V)/W
       
RCs = RCs.reshape(shape)


plt.figure(3)
a = plt.contour(np.power(V,2)/2/9.81,H,He,5,colors='k', linewidths = 0.5)
b = plt.contour(np.power(V,2)/2/9.81,H,RCs,20,colors='k')
plt.plot(206**2/2/9.81,20000,'k o')
plt.clabel(b, inline=1, fontsize=10)
plt.show()