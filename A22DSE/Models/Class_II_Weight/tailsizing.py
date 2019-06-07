# -*- coding: utf-8 -*-
"""
Created on Thu May 16 17:53:19 2019

@author: lujingyi
"""
from math import sqrt,radians,tan,cos
#-----------------------Conventional Tail-------------------------------------
def ctail(Aircraft):
    anfp = Aircraft.ParAnFP
    Layout=Aircraft.ParLayoutConfig
    x_lemacw=Layout.x_lemac
    Sw = anfp.S
    MAC = anfp.MAC
    Aw = anfp.A
    b = sqrt(Sw*Aw)
    Vc = anfp.V_cruise
    Vd = 1.4*Vc   #dive speed !!!FIND REFERENCE!!!
    Kh = 1 #1.0 for fixed incidence stabilizers; 1.1 for variable incidence stabilizers
    Kv = 1
    #--------------horizontal tail----------- 
    Sh = 0.2917*Sw-1.1666  #statistics linear relationship 0.2917*Sw-1.1666
    Vh = 1.1  #statstics average
    xh = Vh*Sw*MAC/Sh
    Ah = 4.16
    trh = 0.348
    Lambda25h = 33.3
    bh = sqrt(Sh*Ah)
    crh = 2*Sh/bh/(1+trh)
    cth = crh*trh
    Lambda50h = (0.5*bh*tan(radians(Lambda25h))+0.25*cth-0.25*crh)/(0.5*b)
    Wht = Kh*(Sh*10.764)*(3.81*((Sh*10.764)**0.2*(Vd/0.5144)/1000/(cos(Lambda50h))**0.5)-0.287)*0.4536
    mac_h = (2./3.) * crh * (1. + trh + trh**2.)/(1. + trh)
    y_MACh=bh*2/6*((1+2*trh)/(1+trh))

    #print(Lambda50h,Wht)
    #--------------vertical tail-------------
    Sv = 0.1446*Sw+5.2406  #statistics linear relationship 0.1446*Sw+5.2406
    Vv = 0.06   #statstics average
    xv = Vv*Sw*b/Sv
    Av = 1.79
    trv = 0.311
    Lambda25v = 39
    bv = sqrt(Sv*Av)
    crv = 2*Sv/bv/(1+trv)
    ctv = crv*trv
    Lambda50v = (bv*tan(radians(Lambda25v))+0.25*ctv-0.25*crv)/bv
    Wvt = Kv*(Sv*10.764)*(3.81*((Sv*10.764)**0.2*(Vd/0.5144)/1000/(cos(Lambda50v))**0.5)-0.287)*0.4536
    mac_v= (2./3.) * crv * (1. + trv + trv**2.)/(1. + trv)
    y_MACv=bv*2/6*((1+2*trv)/(1+trv))

    #print(Lambda50v,Wvt)
    return(Sh,xh,Ah,trh,crh,cth,bh,Lambda25h,Wht,Sv,xv,Av,trv,crv,ctv,bv,Lambda25v,Wvt,mac_h,mac_v,y_MACh,y_MACv)
    
    
    


#-----------------------------T tail------------------------------------------
def ttail(Aircraft):
    anfp = Aircraft.ParAnFP
    Sw = anfp.S
    MAC = anfp.MAC
    Aw = anfp.A
    b = sqrt(Sw*Aw)
    Vc = anfp.V_cruise
    Vd = 1.4*Vc   #dive speed !!!FIND REFERENCE!!!
    Kh = 1 #1.0 for fixed incidence stabilizers; 1.1 for variable incidence stabilizers
    Kv = 1
    zh = 4.5 
    #--------------horizontal tail----------- 
    Sh = 0.2917*Sw-1.1666  #statistics linear relationship 0.1446*Sw+5.2406
    Vh = 1.25 #statstics average
    xh = Vh*Sw*MAC/Sh
    Ah = 4.15
    trh = 0.442
    Lambda25h = 28.2
    bh = sqrt(Sh*Ah)
    crh = 2*Sh/bh/(1+trh)
    cth = crh*trh
    Lambda50h = (0.5*bh*tan(radians(Lambda25h))+0.25*cth-0.25*crh)/(0.5*b)
    Wht = Kh*(Sh*10.764)*(3.81*((Sh*10.764)**0.2*(Vd/0.5144)/1000/(cos(Lambda50h))**0.5)-0.287)*0.4536
    #print(Lambda50h,Wht)
    #--------------vertical tail-------------
    Sv = 0.1446*Sw+5.2406  #statistics linear relationship 0.1446*Sw+5.2406
    Vv = 0.06   #statstics average
    xv = Vv*Sw*b/Sv
    Av = 1.3
    trv = 0.646
    Lambda25v = 40.2
    bv = sqrt(Sv*Av)
    crv = 2*Sv/bv/(1+trv)
    ctv = crv*trv
    Lambda50v = (bv*tan(radians(Lambda25v))+0.25*ctv-0.25*crv)/b
    Wvt = (Kv+0.15*Sh*zh/Sv/bv)*(Sv*10.764)*(3.81*((Sv*10.764)**0.2*(Vd/0.5144)/1000/(cos(Lambda50v))**0.5)-0.287)*0.4536
    #print(Lambda50v,Wvt)
    return(Sh,xh,Ah,trh,crh,cth,bh,Lambda25h,Wht,Sv,xv,Av,trv,crv,ctv,bv,Lambda25v,Wvt) 

  
    
    
  

