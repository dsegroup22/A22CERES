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

#from A22DSE.Parameters.Par_Class_Conventional import Conv
#from A22DSE.Parameters.Par_Class_Atmos import Atmos

anfp = Conv.ParAnFP
struc = Conv.ParStruc
prop = Conv.ParProp
payload = Conv.ParPayload

ISA_model = Atmos()

def Lowbypass(Aircraft, Fsl, ISA_model, H, M):
    Tamb, Pamb = ISA_model.ISAFunc([H])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*M**2)
    delta0 = Pamb/101325*(1+0.4/2*M**2)**(1.4/0.4)
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
            p[i] = 22.65*np.exp(1.73-0.000157*h[i])
    rho = np.multiply(p ,1/(0.2869*(T+273.1)))
    return T, rho, p

SFC = 26.25  * 10**-6 #kg/s/N
MThrust = 60*10**3 #N

n_engines = prop.N_engines

W = (struc.MTOW) * 9.81 

S = anfp.S
CD0 = anfp.CD0

A = anfp.A
e = anfp.e
K = 1/m.pi/A/e

"""Minimum time climb"""
#Max RC

res = 500
res1 = 100
z=res*100
H = np.linspace(10,23000,res)
V = np.linspace(10,250,res)
V, H =  np.meshgrid(V,H)
shape = H.shape
MaxT = np.ones(shape)
rho = getatm(np.ravel(H))[1]
T = getatm(np.ravel(H))[0]
#setting = np.linspace(0.2,1,res)
Thrust = np.ones(res)


M = np.ravel(V)/np.sqrt(1.4*287*(273.15+T))
H = np.ravel(H)
#MaxT = np.ravel(MaxT)
#for i in range(len(np.ravel(H))):
#    MaxT[i] = Lowbypass(Conv,MThrust, ISA_model,H[i], anfp.Mdd)
MaxT = MaxT.reshape(shape)
rho = rho.reshape(shape)
for i in range(len(MaxT[0])):
    MaxT[i,:] = MThrust * rho[i,0]/rho[0,0] -0.2
#    MaxT[:,i] = Thrust

He = np.ravel(H) + np.power(np.ravel(V),2)/2/9.81

#tminopt = 1000
#fuelopt = 15000
CLopt = 0
Vopt = None
Hopt = None
RCsopt = None
Fly = None


CLmin = 1.1* W /(0.5*np.ravel(rho)*np.ravel(V)**2*S)

CL = np.minimum(1/2/K*((-np.ravel(MaxT)/W)+np.sqrt((np.ravel(MaxT)/W)**2+12\
                        *CD0*K)),CLmin)


RCs = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)*S*\
       (CD0+np.ravel(CL)**2/m.pi/A/e))*np.ravel(V)/W
       
CL = CL.reshape(shape)
       
RCs = RCs.reshape(shape)  
He = He.reshape(shape)
H = H.reshape(shape)
V = V.reshape(shape)     



#tclimb=np.zeros((res))

He_ar = np.linspace(2000,22162.895,res1)
RCs_tmin = np.zeros(1)
V_tmin = np.zeros(1)
H_tmin = np.zeros(1)
thrust_tmin = np.zeros(1)
FinalRCs = np.zeros(1)
mass=0
Energy=np.zeros(1)
i=0
t=30
time = 0
CL_tmin =np.zeros(1)
#for i in range(len(He_ar)):
#He = 22162.895
while 20000 > H_tmin[-1] and i < 600:
#    print(i)
    W = W - mass*9.81
    CLmin = 1.1* W /(0.5*np.ravel(rho)*np.ravel(V)**2*S)
    CLmax = anfp.CLMAX*.9
    CL1 = np.minimum(1/2/K*((-np.ravel(MaxT)/W)+np.sqrt((np.ravel(MaxT)/W)**2+12\
                        *CD0*K)),CLmax*np.ones(CLmin.shape))
    CL = np.maximum(CLmin, CL1)
    CL = CL.reshape(shape)
    Vmin  = (1.1*W/(0.5*rho[:,0]*anfp.CLMAX*S))**0.5
#    V = np.maximum(Vmin,np.ravel(V))
#    V = np.minimum(np.ones(res**2)*anfp.V_cruise,V)
    
    RCs = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)*S*\
       (CD0+np.ravel(CL)**2/m.pi/A/e))*np.ravel(V)/W
    RCs = RCs.reshape(shape)
    V = V.reshape(shape)
    RCsi=RCs[np.where(np.logical_and(Energy[-1]> He-z/res \
                          , Energy[-1] < He+z/res))]
    RCsapp = RCsi[np.logical_not(np.isnan(RCsi))]
    RCs_tmin = np.append(RCs_tmin,np.amax(RCsapp))
#    print(RCs_tmin[-1])
    index=(int(np.where(RCs == RCs_tmin[-1])[0]),\
    int(np.where(RCs == RCs_tmin[-1])[1]))
#    print(V[index] < Vmin[index[0]])
    if V[index] < Vmin[index[0]]:
        V_tmin = np.append(V_tmin,Vmin[-1])
        H_tmin = np.append(H_tmin,H_tmin[-1])
        thrust_tmin = np.append(thrust_tmin,thrust_tmin[-1])
        FinalRCs = np.append(FinalRCs,0)
    else:
        thrust_tmin = np.append(thrust_tmin,MaxT[index])
        
        V_tmin = np.append(V_tmin,V[index])
        H_tmin = np.append(H_tmin,H_tmin[-1]+RCs_tmin[-1]*t)
        FinalRCs = np.append(FinalRCs,RCs_tmin[-1])
    CL_tmin = np.append(CL_tmin,CL[index]    )
    mass=thrust_tmin[-1]*SFC*n_engines*t
    if H_tmin[-1] > 19500:
        mass+=0.827*t
    time +=t
        
    Energy = np.append(Energy, H_tmin[-1] + V_tmin[-1]**2/2/9.81)
#    print(Energy[-1], RCs_tmin[-1])
    i +=1
index = np.where(np.logical_and(V_tmin < 220, np.logical_and(FinalRCs !=None , FinalRCs !=0)))
tmin = float(np.trapz(np.divide(1,FinalRCs[index]),Energy[index]))/60
fuelopt = 100000000
fuel = float(np.trapz(np.divide(thrust_tmin[index],FinalRCs[index]),Energy[index]))*SFC*n_engines
if fuel < fuelopt:
    fuelopt = fuel
    CLopt = CL_tmin[index]
    tminopt = tmin
    Vopt = V_tmin[index]
    Hopt = H_tmin [index]
    RCsopt = RCs_tmin[index]
    EnergyOpt = Energy[index]
#    Fly = (anfp.CLMAX*np.ones(res**2) > CLopt)

#i=0
#massi = np.zeros(0)
#while RCs[450,435]<0.1:
#    
#    CLmin = 1.1* W /(0.5*np.ravel(rho)*np.ravel(V)**2*S)
#
#    CL = CLmin
#    
#    RCs = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)*S*\
#       (CD0+np.ravel(CL)**2/m.pi/A/e))*np.ravel(V)/W
#    RCs = RCs.reshape(shape)
#    RCs_tmin = np.append(RCs_tmin,0)
#    V_tmin = np.append(V_tmin,V_tmin[-1])
#    H_tmin = np.append(H_tmin, H_tmin[-1])
#    thrust_tmin = np.append(thrust_tmin, thrust_tmin[-1])
#    mass=thrust_tmin[-1]*SFC*n_engines*100
#    W = W - mass*9.81   
##    print(RCs[450,434], W/9.81)
#    i+=1
#    massi = np.append(massi,mass)
#       
#       
#       
#       
#       
#       
#       
#tmin = tmin + 10*i/60
#fuel = fuel + np.trapz(massi, dx = 1)


rho = rho.reshape(shape)
plt.figure(1)
a = plt.contour(np.power(V,2)/2/9.81,H,He,5,colors='k', linewidths = 0.5)
b = plt.contour(np.power(V,2)/2/9.81,H,RCs,20,colors='k')
plt.plot(np.power(Vopt,2)/2/9.81,Hopt)
plt.plot(anfp.V_cruise**2/2/9.81,20000,'k o')
#plt.plot(np.ones(res)*129**2/2/9.81,H[:,0])
plt.plot((1.1*W/(0.5*rho[:,0]*anfp.CLMAX*S))/2/9.81,H[:,0])
plt.clabel(b, inline=1, fontsize=10)
plt.xlabel(r'$\frac{V^2}{2g_0}$ [m]')
plt.ylabel(r'Altitude H [m]')
#plt
plt.show()
#
#
plt.figure(2)
a = plt.plot(EnergyOpt, np.divide(1,RCsopt))
plt.title('Climb time ='+ str(float(np.trapz(np.divide(1,RCsopt),EnergyOpt))\
                              /60)+'min')
plt.show()
#print(RCs[434,450])
# 
#
#W = (struc.MTOW ) * 9.81
#CLnew = np.minimum(1/2/K*((-np.ravel(MaxT)/W)+np.sqrt((np.ravel(MaxT)/W)\
#                           **2+12*CD0*K)),np.ones(np.ravel(He).shape)*CLmaxAllow)
#
#RCsnew = (np.ravel(MaxT)*n_engines-0.5*np.ravel(rho)*np.power(np.ravel(V),2)\
#          *S*(CD0+np.ravel(CLnew)**2/m.pi/A/e))*np.ravel(V)/W
#       
#CLnew = CLnew.reshape(shape)
#
#       
#RCsnew = RCsnew.reshape(shape)
#
#
#plt.figure(3)
#a = plt.contour(np.power(V,2)/2/9.81,H,He,10,colors='k', linewidths = 0.5)
#b = plt.contour(np.power(V,2)/2/9.81,H,RCsnew,20,colors='k')
#plt.plot(anfp.V_cruise**2/2/9.81,20000,'k o')
#plt.clabel(b, inline=1, fontsize=10)
#plt.show()
