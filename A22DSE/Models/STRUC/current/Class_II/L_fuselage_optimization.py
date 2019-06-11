# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 21:04:59 2019

@author: lujingyilu
"""

from math import cos,tan,sqrt,radians,pi,degrees
from FuselageLength import GetTotalFuselageLength
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

def fuselageopt(Aircraft,xht):
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig
    
#    xht = 20
    xvt = xht
    tailarm = xht
    l_freq = Conv.ParLayoutConfig.x_oe*Conv.ParAnFP.MAC+tailarm*1.8
    
#    l_freq = Conv.ParLayoutConfig.x_lemac+Conv.ParLayoutConfig.x_oe*Conv.ParAnFP.MAC+tailarm
    h_fuselage=config.h_fuselage    #[m]
    w_fuselage=config.w_fuselage    #[m]
    a=GetTotalFuselageLength(Conv, l_freq, 2, 0.01)   #[m]
    l_fuselage = sum(a[0])
    
    
#    torenbeek method  (Chapter 8.3.3)  
    l_ref=1.5 #[m]
    n_ult=anfp.n_ult
    d_fuselage=np.average([h_fuselage,w_fuselage])    
    
    C_shell=60          #[N/m^3]
    Omega_fl=160        #[N/m^2]
    
    W_shell=C_shell*d_fuselage**2*l_fuselage
    W_bulkheads=C_shell*d_fuselage**2*l_ref
    
    W_fl=Omega_fl*n_ult**0.5*d_fuselage*l_fuselage
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
    deltar = radians(40)
    CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar 
    rho = 1.225  #takeoff air density
    Vmc = 1.13*Aircraft.ParAnFP.V_stall   #1.13*vstall!!!!!!
    Svi = 0.5*Aircraft.ParAnFP.T_to*Aircraft.ParLayoutConfig.y_engine/(lvi*0.5*rho*Vmc**2*CLv)
    anfp = Aircraft.ParAnFP
    Vc = anfp.V_cruise
    Kv = 1
    Wvt = Kv*(Svi*10.764)*(3.81*((Svi*10.764)**0.2*(Vd/0.5144)/1000/(cos(swhalf))**0.5)-0.287)*0.4536   
    return(W_f_tor+mh+Wvt,Sh,Svi,l_fuselage)
    
Wtab = []
Shtab = []
Svtab = []
Lftab = []
xhttab = list(range(5,35,1))
for xht in range(5,35,1):
    Wtab.append(fuselageopt(Conv,xht)[0])
    Shtab.append(fuselageopt(Conv,xht)[1])
    Svtab.append(fuselageopt(Conv,xht)[2])
    Lftab.append(fuselageopt(Conv,xht)[3])
plt.subplot(221)
plt.plot(xhttab,Wtab)
plt.xlabel('tail arm [m]')
plt.ylabel('Weight of Fuselage and Tail [kg]')
plt.subplot(222)
plt.plot(xhttab,Lftab)
plt.xlabel('tail arm [m]')
plt.ylabel('Fuselage Length [m]')
plt.subplot(223)
plt.plot(xhttab,Shtab)
plt.xlabel('tail arm [m]')
plt.ylabel('Horizontal Tail Surface Area [m^2]')
plt.subplot(224)
plt.plot(xhttab,Svtab)
plt.xlabel('tail arm [m]')
plt.ylabel('Vertical Tail Surface Area [m^2]')
plt.show()

