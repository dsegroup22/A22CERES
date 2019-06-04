# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:07:45 2019

@author: lujingyi
"""
from math import pi,radians,sqrt,tan,atan,degrees
def vtailII(Aircraft):
    lvi = Aircraft.ParLayoutConfig.xvt+6.5
    Svi = Aircraft.ParLayoutConfig.Svt-2.4
    Avi = Aircraft.ParLayoutConfig.Avt+0.5
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
    tauc = 0.4    #cr/cv !!!!!!
    taub = 1      #br/bv
    CLvdeltar = CLvbeta*tauc*taub
    CLv0 = 0   #because of the symmetric airfoil
    beta = radians(5)   
    deltar = radians(40)
    CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar 
    rho = 1.225  #takeoff air density
    Vmc = 45   #1.13*vstall!!!!!!
    Lv = 0.5*rho*Vmc**2*Svi*CLv
    oeidif =Lv*lvi-90000*4.5#Aircraft.ParLayoutConfig.y_loc_eng
    VL = 40  #landing speed !!!!!!!!!
    Vw = 12.861   #CS25 Mximum crosswind velocity (90degree)
    betaw = atan(Vw/VL)
    lac = 2    #distance between the side geometric center and landing center of gravity
    CLvw = CLv0 + CLvbeta*betaw+CLvdeltar*deltar
    Lv = 0.5*rho*(VL**2+Vw**2)*Svi*CLv
    Sside = 150   #side surface area!!!!!!!!
    CDside = 0.65
    Fw = 0.5*rho*Vw**2*Sside*CDside
    cwdif = Lv*lvi-Fw*lac
    return(oeidif,cwdif)
    
    