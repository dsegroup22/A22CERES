# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:21:46 2019

@author: menno
"""

Cruise=False
LowSpeed=False



#Cruise=True
LowSpeed=True




import matplotlib.pyplot as plt
plt.clf()
import numpy as np
import sys
sys.path.append('../../')
from A22DSE.Parameters.Par_Class_Diff_Configs import Conv
from A22DSE.Models.AnFP.Current.Class_II.WingDesign.C_L_curve import (C_L_CurveCruise,C_L_CurveLowSpeed)
anfp=Conv.ParAnFP
As=np.array([8,11,anfp.A])
colors=np.array(['r','g','b','k'])
i=0
for A in As:
    anfp.A=A
    if Cruise:
        alpha_0,C_L_alpha,C_L_max,alpha_stall=C_L_CurveCruise(Conv)
        M=0.6
    if LowSpeed:
        alpha_0,C_L_alpha,C_L_max,alpha_stall=C_L_CurveLowSpeed(Conv)
        M=0.2
    alpha_linstall=C_L_max/C_L_alpha+alpha_0
    lbl='M='+str(M)+' '+ 'A= '+str(A)
    if i==2:
        lbl='M='+str(M)+' '+ 'A= '+str(A) +' (Current Design Point)'
    plt.plot([alpha_0*180/np.pi,alpha_linstall*180/np.pi],[0,C_L_max],colors[i],label=lbl)
    plt.plot([alpha_stall*180/np.pi],[C_L_max],colors[i]+'o')
    i+=1
beta=np.sqrt(1-M**2)
C_L_alpha=anfp.cl_alpha*180/np.pi/beta
C_L_max=anfp.cl_max/beta
alpha_stall=anfp.alpha_stall-C_L_max/C_L_alpha*(1-1/beta)

alpha_linstall=C_L_max/C_L_alpha+alpha_0
plt.plot([alpha_0*180/np.pi,alpha_linstall*180/np.pi],[0,C_L_max],colors[i]+'--',\
             label='Airfoil (M= '+str(M)+ ' A= '+r'$\infty$)')
plt.plot([alpha_stall*180/np.pi],[C_L_max],colors[i]+'o')

plt.plot([],[],'ko',label='Actual non-linear stall')

plt.title('Lift Curve for Complete Wing',fontsize=16)
plt.xlabel(r'$\alpha$ [°]',fontsize=12)
plt.ylabel('$C_{L}$ [-]',fontsize=12)
plt.axvline(color='k')
plt.axhline(color='k')
plt.legend(loc='upper left',fontsize=10)
plt.tick_params(axis='both',labelsize=12)

plt.show()

