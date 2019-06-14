# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 10:41:32 2019

@author: tomhu
"""

import numpy as np
import matplotlib.pyplot as plt
import math as m
import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])

#from A22DSE.Parameters.Par_Class_Conventional import Conv

anfp = Conv.ParAnFP
struc = Conv.ParStruc
prop = Conv.ParProp
payload = Conv.ParPayload
layout = Conv.ParLayoutConfig

L = layout.l_fuselage
X = np.linspace(0,1, 100)
D = layout.w_fuselage
fr = L / D
Xm = layout.x_cg[1]+m.cos(m.radians(8)) #lg main distance
Xi = Xm + 5
Ri = D/2-0.1
Rn = 5
Si = 100
phi = m.radians(11)
K1 = 0.05
xm = Xm/L
xi = Xi/L
k1 = -2*xm*fr*K1*L
ri = 2*fr*Ri/L
rn = 4*xm*fr*Rn/L
si = (-2*fr*(xi-xm)/(L-ri))*Si
r = np.zeros(X.shape)
x = np.zeros(X.shape)

for i in range(len(X)):    
    if X[i] >= 0 and X[i] < xm:
        x[i] = X[i]/xi
        F1 = -2*x[i]*(x[i]-1**3)
        F2 = -x[i]**2*(x[i]-1)**2
        G = x[i]**2*(3*x[i]**2-8*x[i]+6)
        r[i] = (1/2/fr)*(rn*F1 + k1*F2 + G)**0.5
    if xm <= X[i] and X[i]<xi:
        x[i] = (xi-X[i])/(xi-xm)#(Xi-X[i])/(Xi-Xm)
        F1 = -0.5*x[i]**3*(x[i]-1)**2
        F2 = x[i] - x[i]**3*(3*x[i]**2-8*x[i]+6)
        G = x[i]**3*(6*x[i]**2-15*x[i]+10)
        k1m = ((xi/xm)-1)**2*k1/(1-ri)
        r[i] = (1/2/fr)*(ri + (1-ri)*(k1m*F1+si*F2+G))*1.4
    if xi <= X[i] and X[i]<= 1:
        x[i] =1-X[i]#/L
        siL = (2*fr*(xi-xm)*m.tan(phi))/(1-ri)
        sia = (1-ri)*(1-xi)*si/(xi-xm)/ri
        r[i] = (siL*x[i]*(1-x[i]**3)-sia * x[i]**2*(2*x[i]-3)*(x[i]-1)\
        + x[i]**2*(3*x[i]**2-8*x[i]+6))/75
    
    
    
R = r*L   
plt.figure(1)
plt.plot(np.linspace(0,L,len(r)), R)
plt.plot(np.linspace(0,L,len(r)), -R)
plt
plt.axis('equal')
plt.show()    
