# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 21:04:59 2019

@author: lujingyilu
"""

from math import cos,tan,sqrt,radians,pi,degrees
#from FuselageLength import GetTotalFuselageLength

from A22DSE.Models.STRUC.current.Class_II.FuselageLength import GetTotalFuselageLength

import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

def fuselageopt(Aircraft,xht,deltarin):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
    
#    xht = 20
    xvt = xht
    tailarm = xht
    l_freq = config.x_cg[1] + xht #Aircraft.ParLayoutConfig.x_oe*Conv.ParAnFP.MAC+tailarm*1.8
    
#    l_freq = Conv.ParLayoutConfig.x_lemac+Conv.ParLayoutConfig.x_oe*Conv.ParAnFP.MAC+tailarm
    h_fuselage=config.h_fuselage    #[m]
    w_fuselage=config.w_fuselage    #[m]

    a=GetTotalFuselageLength(Aircraft, l_freq, 2, 0.01)   #[m]
    l_fuselage = sum(a[0])

    
    
#    torenbeek method  (Chapter 8.3.3)  
    l_ref=1.5 #[m]
    n_ult=anfp.n_ult
    d_fuselage=np.average([h_fuselage,w_fuselage])    
    
    C_shell=60          #[N/m^3]
    Omega_fl=160        #[N/m^2]
    
    W_shell=C_shell*d_fuselage**2*l_freq
    W_bulkheads=C_shell*d_fuselage**2*l_ref
    
    W_fl=Omega_fl*n_ult**0.5*d_fuselage*l_freq
    W_f_tor=W_shell+W_bulkheads+W_fl
    
    
    #tail
    Vh = 1
    MAC = anfp.MAC
    Sw = anfp.S
    kh = 1.1
    Vd = anfp.V_dive
    Sh = Vh*MAC*Sw/tailarm
    sweep_h50 = config.sweep50ht
    mh = kh*Sh*(62*(Sh**0.2*Vd)/(1000*sqrt(cos(sweep_h50)))-2.5)
    
    lvi = xvt
    Sv = Aircraft.ParLayoutConfig.Svt
    Avi = Aircraft.ParLayoutConfig.Avt
    trvi = Aircraft.ParLayoutConfig.trvt
    swquart = Aircraft.ParLayoutConfig.Sweep25vt
    M = Aircraft.ParAnFP.M_cruise
    betav = sqrt(1-M**2)
    etha = 0.95
    bv = sqrt(Sv*Avi)
    crv = 2*Sv/bv/(1+trvi)
    ctv = crv*trvi
    swhalf = (bv*tan(radians(swquart))+0.25*ctv-0.25*crv)/bv
    CLvbeta= 2*pi*Avi/(2.+ sqrt(4.+Avi*(betav/etha)**2*(1.+(tan(radians(swhalf))/betav)**2)))
    Vv = lvi*Sv/Aircraft.ParAnFP.S/Aircraft.ParAnFP.b
    tauc = 0.4    #cr/cv 
    taub = 1      #br/bv
    CLvdeltar = CLvbeta*tauc*taub
    CLv0 = 0   #because of the symmetric airfoil
    beta = radians(5)   
    deltar = radians(deltarin)
    CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar 
    rho = 1.225  #takeoff air density
    Vmc = 1.13*Aircraft.ParAnFP.V_stall   #1.13*vstall!!!!!!
    Svi = Aircraft.ParAnFP.T_to/Aircraft.ParStruc.N_engines*\
    Aircraft.ParLayoutConfig.y_eng_out/(lvi*0.5*rho*Vmc**2*CLv)
    anfp = Aircraft.ParAnFP
    Vc = anfp.V_cruise
    Kv = 1
    Wvt = Kv*(Svi*10.764)*(3.81*((Svi*10.764)**0.2*(Vd/0.5144)/1000/(cos(swhalf))**0.5)-0.287)*0.4536   
    return(W_f_tor+mh+Wvt)
    
Wtab = []
#Shtab = []
#Svtab = []
#Lftab = []
xhttab = list(range(5,40,5))
deltartab = list(range(0,45,5))
Wtab = np.zeros(len(deltartab))
for xht in range(5,40,5):
#    print('hi')

    Wtabsub = np.array([])
    for deltarin in range(0,45,5):
        Wtabsub = np.append(Wtabsub,fuselageopt(Conv,xht,deltarin))
    Wtab = np.vstack((Wtab,Wtabsub))
Wtab = Wtab[1:]
#print(Wtab)
#        print(fuselageopt(Conv,xht,deltarin))
#        Wtab.append(fuselageopt(Conv,xht,deltarin))
#    Shtab.append(fuselageopt(Conv,xht)[1])
#    Svtab.append(fuselageopt(Conv,xht)[2])
#    Lftab.append(fuselageopt(Conv,xht)[3])
  

#contours=plt.contour(deltartab,xhttab,Wtab,levels=[0,75000,100000,125000,150000])
#plt.clabel(contours, inline=True, fontsize=14)
#plt.contourf(deltartab,xhttab,Wtab,cmap='Greys',levels=500)
#plt.colorbar()
##plt.title(Weight,fontsize=18,horizontalalignment='center')
#plt.tick_params(labelsize=14)
#plt.xlabel('$\delta_{r}$ [$^{\circ}$]',fontsize=14)
#plt.ylabel('Tail Arm [m]',fontsize=14)
#plt.show()






#plt.figure(1)
#plt.plot(xhttab,Lftab)
#plt.xlabel('Tail arm [m]')
#plt.ylabel('Fuselage Length [m]')
#plt.figure(2)
#plt.plot(xhttab,Shtab)
#plt.xlabel('Tail arm [m]')
#plt.ylabel('Horizontal Tail Surface Area [$m^2$]')
#plt.show()
#
    
#fig, ax1 = plt.subplots()
#color = 'tab:red'
#ax1.set_xlabel('Tail arm [m]')
#ax1.set_ylabel('Surface Area [$m^2$]', color='purple')
#ax1.plot(xhttab,Shtab,color='purple',label='Sh')
#ax1.plot(xhttab,Svtab,'--',color='purple',label='Sv')
#ax1.tick_params(axis='y',labelcolor='purple')
#
#
#ax2 = ax1.twinx()
#
#ax2.set_ylabel('Fuselage Length [m]', color='crimson')
#ax2.plot(xhttab,Lftab,color='crimson',label='$l_{fuselage}$')
#ax2.tick_params(axis='y',labelcolor='crimson')
#
#
##fig.tight_layout()
#plt.title('Sensitivity of Tail Arm')
##plt.legend( lines, labels, loc = 'lower center', bbox_to_anchor = (0,-0.1,1,1),
#          #  bbox_transform = plt.gcf().transFigure )
#fig.legend(bbox_to_anchor = (-0.1,-0.12,1,1))
#plt.show()


#plt.figure(1)
#plt.plot(xhttab,Wtab)
#plt.xlabel('Tail arm [m]')
#plt.ylabel('Weight of Fuselage and Tail [kg]')

plt.figure(2)
plt.plot(xhttab,Wtab)
plt.xlabel('Tail arm [m]')
plt.ylabel('Weight of Fuselage and Tail [kg]')
plt.title('Fuselage & Tail Weight vs Tail Arm')

#plt.figure(2)
#plt.plot(xhttab,Lftab)
#plt.xlabel('Tail arm [m]')
#plt.ylabel('Fuselage Length [m]')
#plt.figure(3)
#plt.plot(xhttab,Shtab)
#plt.xlabel('Tail arm [m]')
#plt.ylabel('Horizontal Tail Surface Area [$m^2$]')
#plt.figure(4)
#plt.plot(xhttab,Svtab)
#plt.xlabel('Tail arm [m]')
#plt.ylabel('Vertical Tail Surface Area [$m^2$]')
#plt.show()

