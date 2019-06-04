# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:07:45 2019

@author: lujingyi
"""
from math import pi,radians,sqrt,tan
def vtailII(Aircraft):
    lvi = Aircraft.ParLayoutConfig.xvt+3
    Svi = Aircraft.ParLayoutConfig.Svt
    Avi = Aircraft.ParLayoutConfig.Avt+0.7
    trvi = Aircraft.ParLayoutConfig.trvt
    swquart = Aircraft.ParLayoutConfig.Sweep25vt
    M = Aircraft.ParAnFP.M_cruise
    betav = sqrt(1-M**2)
    etha = 0.95
    bv = sqrt(Svi*Avi)
    crv = 2*Svi/bv/(1+trvi)
    ctv = crv*trvi
    swhalf = (bv*tan(radians(swquart))+0.25*ctv-0.25*crv)/bv
    CLvbeta= 2*pi*Avi/(2.+ sqrt(4.+Avi*(betav/etha)**2*(1.+(tan(radians(swhalf))/betav)**2)))
    Vv = lvi*Svi/Aircraft.ParAnFP.S/Aircraft.ParAnFP.b
    tauc = 0.35    #cr/cv !!!!!!
    taub = 1      #br/bv
    CLvdeltar = CLvbeta*tauc*taub
    CLv0 = 0   #because of the symmetric airfoil
    beta = radians(5)   
    deltar = radians(45)
    CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar 
    rho = 1.225  #takeoff air density
    Vmc = 45   #1.13*vstall
    Lv = 0.5*rho*Vmc**2*Svi*CLv
    dif =Lv*lvi-90000*4.5#Aircraft.ParLayoutConfig.y_loc_eng
    
    print(CLv,dif,Avi)
    
    