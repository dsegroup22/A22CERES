# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:59:28 2019

@author: tomhu
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

res = 50

l = 10 #m between surfaces
cm0c = -0.04
cm0w = -0.04
cmalpha = -0.8

aspect_eval = False

S = 140
dist = 0.10
Sw0 = (1-dist) * S
Sc0 = dist * (S)
Ac0 = 17.5
Aw0 = 20


CLcruise = 0.67

if aspect_eval == True:
    Aw = np.linspace(1,Aw0,res)
    Ac = np.linspace(1,Ac0,res)

    Aw,Ac = np.meshgrid(Aw,Ac)   
    if Sw0 != False and Sc0 !=  False:
        Sw, Sc = Sw0 * np.ones(Aw.shape), Sc0*np.ones(Ac.shape)


else:
    Sw = np.linspace(1,S-1,res)
    Sc = S - Sw
  
    if Sw0 != False and Sc0 !=  False:
        Aw, Ac = Aw0 * np.ones(Sw.shape), Ac0*np.ones(Sc.shape)


down =0.15

CLc = np.array([])
CLw = np.array([])

for Aci,Awi,Sci,Swi in np.dstack((np.ravel(Ac),np.ravel(Aw), np.ravel(Sc), np.ravel(Sw)))[0]:
    dalpha = np.sqrt(Aci*Sci/Awi/Swi)*(1-down) + (1-np.sqrt(Aci*Sci/Awi/Swi))
    if dalpha < (1-down):
        dalpha = 1-down
    k = Swi*dalpha/(Sci+Swi*dalpha)
    A = np.matrix([[Sci, Swi],[Sci*k*l,-Swi*(1-k)*l]])
    B = np.matrix([[CLcruise*(Swi+Sci)],[-cm0c*np.sqrt(Sci/Aci)-cm0w*np.sqrt(Swi/Awi)]])
    Aminus = np.linalg.inv(A)
    CL = Aminus*B
    if CL[0,0] > CL[1,0]:
        CLc = np.append(CLc,CL[0,0])
        CLw = np.append(CLw,CL[1,0])
    else:
        CLc = np.append(CLc,10000)
        CLw = np.append(CLw,10000)
    



Ae = (CLcruise)**2/(np.ravel(CLc)**2/np.ravel(Ac)*np.ravel(Sc)/(np.ravel(Sc)+np.ravel(Sw))+np.ravel(CLw)**2/np.ravel(Aw)*np.ravel(Sw)/(np.ravel(Sc)+np.ravel(Sw)))



print('Maximum equivalent aspect ratio is', max(Ae))

if aspect_eval == True:

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')


    Ae = Ae.reshape(Sw.shape)
    Aw = Aw.reshape(Sw.shape)
    Ac = Ac.reshape(Sc.shape)

    ax.plot_wireframe(Aw, Ac, Ae, color = 'y')

    ax.set_xlabel('AR Aft')
    ax.set_ylabel('AR Fwd')
    ax.set_zlabel('Ae')

else:
    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.scatter(Sw/(Sc+Sw), Ae, color = 'y')
    ax.plot(Sw/(Sc+Sw), Ae, color = 'y')

    ax.set_xlabel('Aft Surface Area Ratio')
    ax.set_ylabel('Ae')


plt.show()



