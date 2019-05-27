# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:59:28 2019

@author: tomhu
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math

#CLmax = 1.5
res = 100

#rho = 0.0887
#CLcruise = 0.65
#MTOW = 36 * 10**3*9.81
#Vcruise = 0.72 * (1.4*287*(273.15-56.46))**0.5


#Scanard = []
#Swing = []
#CLcanard = []
#CLwing = []
#S = []
#dist = np.linspace(0.1,0.5,res)

#for i in range(len(dist)):  
##    print(dist)
#    Sc = dist[i]*MTOW / (CLcruise*0.5*rho*Vcruise**2)
#    Sw = (1-dist[i])*MTOW / (CLcruise*0.5*rho*Vcruise**2)
##    print(Sc)
#    CLc = MTOW / (0.5*rho*Vcruise**2*Sc)
#    CLw = MTOW / (0.5*rho*Vcruise**2*Sw)
#    CLwing.append(CLw)
#    CLcanard.append(CLc)
#    Scanard.append(Sc)
#    Swing.append(Sw)
#    S.append(Sw + Sc)
##    print(S)
#plt.plot(dist,S)
#plt.show()
#print(min(S),Swing[S.index(min(S))],Scanard[S.index(min(S))]) 
bci = False
bwi = False
cci = False
cwi = False
Swi = 200
Sci = 50

Aw = np.linspace(1,20,res)
Ac = np.linspace(1,20,res)
Aw,Ac = np.meshgrid(Aw,Ac)   
if Swi != False and Sci !=  False:
    Sw, Sc = Swi * np.ones(Aw.shape), Sci*np.ones(Ac.shape)

if cci == False:
    bc = (Ac*Sc)**0.5
    cc = Sc/bc
if bci == False:    
    bc = (Ac*Sc)**0.5
    cc = Sc/bc
if cwi == False:
    bw = (Aw*Sw)**0.5
    cw = Sw/bw        
if bwi == False :
    bw = (Aw*Sw)**0.5
    cw = Sw/bw 
    
#Sw = cw*bw        
#            
#Sc = cc*bc                   


#Aw, Ac = bwi**2/np.ravel(Sw), bci**2/np.ravel(Sc)
down = -0.15#2 * 0.0987 /180/np.ravel(Ac)
d = (np.ravel(Ac)*np.ravel(Sc)*np.ravel(Sw)/np.ravel(Aw))**0.5\
*(1-np.ravel(down))+(1-(np.ravel(Ac)*np.ravel(Sc)*np.ravel(Sw)\
             /np.ravel(Aw))**0.5)
     
Ae = (np.ravel(Sc)/np.ravel(Sw)/np.ravel(d))*(1+np.ravel(Sc)/np.ravel(Sw))\
/(1/np.ravel(Aw)+1/np.ravel(Ac)/np.ravel(d)**2)
#        Alstsub.append(Ae)
#Alst.append(Ae)

    
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')



Ae =Ae.reshape(Sw.shape)
Aw = Aw.reshape(Sw.shape)
Ac = Ac.reshape(Sc.shape)
ax.plot_wireframe(Aw, Ac, Ae)
ax.set_xlabel('AR Wing')
ax.set_ylabel('AR Canard')
ax.set_zlabel('Ae')

plt.show()



