# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:07:45 2019

@author: lujingyi
"""
from math import pi,radians,sqrt,tan,atan,degrees,cos
def vtail(Aircraft):
    lvi = Aircraft.ParLayoutConfig.xvt
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
    tauc = 0.4    #cr/cv !!!!!!
    taub = 1      #br/bv
    CLvdeltar = CLvbeta*tauc*taub
    CLv0 = 0   #because of the symmetric airfoil
    beta = radians(5)   
    deltar = radians(40)
    CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar 
    rho = 1.225  #takeoff air density
    Vmc = 45   #1.13*vstall!!!!!!
#    Lv = 0.5*rho*Vmc**2*Sv*CLv
#    oeidif =Lv*lvi-0.5*Aircraft.ParAnFP.T_to*Aircraft.ParLayoutConfig.y_engine#Aircraft.ParLayoutConfig.y_loc_eng
    Svi = 0.5*Aircraft.ParAnFP.T_to*Aircraft.ParLayoutConfig.y_engine/(lvi*0.5*rho*Vmc**2*CLv)



    VL = 40  #landing speed !!!!!!!!!
    Vw = 12.861   #CS25 Mximum crosswind velocity (90degree)
    betaw = atan(Vw/VL)
    lac = 2    #distance between the side geometric center and landing center of gravity
    CLvw = CLv0 + CLvbeta*betaw+CLvdeltar*deltar
    Lv = 0.5*rho*(VL**2+Vw**2)*Sv*CLv
    Sside = 150   #side surface area!!!!!!!!
    CDside = 0.65
    Fw = 0.5*rho*Vw**2*Sside*CDside
    cwdif = Lv*lvi-Fw*lac
    
    
    anfp = Aircraft.ParAnFP
    Vc = anfp.V_cruise
    Vd = 1.4*Vc   #dive speed
    Kv = 1
    Wvt = Kv*(Sv*10.764)*(3.81*((Sv*10.764)**0.2*(Vd/0.5144)/1000/(cos(swhalf))**0.5)-0.287)*0.4536
#    print(oeidif)
    return(Svi,lvi,Avi,trvi,swquart,degrees(swhalf),crv,ctv,bv,Wvt)
    
    