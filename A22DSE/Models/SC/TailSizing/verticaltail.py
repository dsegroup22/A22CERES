# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 19:07:45 2019

@author: lujingyi
"""
from math import pi,radians,sqrt,tan,atan,degrees,cos
def vtail(Aircraft):
    '''
    INPUT: horizontal tail arm, cruise Mach number, preliminary aspect ratio, preliminary taper ratio
           
    '''
    lvi = Aircraft.ParLayoutConfig.xht
    Sv = Aircraft.ParLayoutConfig.Svt
    Avi = 1.3#Aircraft.ParLayoutConfig.Avt
    trvi = 0.646#Aircraft.ParLayoutConfig.trvt
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
    tauc = 0.2    #cr/cv 
    taub = 1      #br/bv
    CLvdeltar = CLvbeta*tauc*taub
    CLv0 = 0   #because of the symmetric airfoil
    beta = radians(5)   
    deltar = radians(25)
    CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar 
    rho = 1.225  #takeoff air density
    Vmc = 1.13*Aircraft.ParAnFP.V_stall   #1.13*vstall!!!!!!
#    Lv = 0.5*rho*Vmc**2*Sv*CLv
#    oeidif =Lv*lvi-0.5*Aircraft.ParAnFP.T_to*Aircraft.ParLayoutConfig.y_engine#Aircraft.ParLayoutConfig.y_loc_eng
    Svi = Aircraft.ParAnFP.T_to/Aircraft.ParStruc.N_engines*Aircraft.ParLayoutConfig.y_eng_out/(lvi*0.5*rho*Vmc**2*CLv)
#    print(Sv,Svi,(abs(Svi-Sv))/Sv)
    
#    if (abs(Svi-Sv))/Sv > 0.1:
#        Sv = Svi
#        bv = sqrt(Sv*Avi)
#        crv = 2*Sv/bv/(1+trvi)
#        ctv = crv*trvi
#        swhalf = (bv*tan(radians(swquart))+0.25*ctv-0.25*crv)/bv
#        CLvbeta= 2*pi*Avi/(2.+ sqrt(4.+Avi*(betav/etha)**2*(1.+(tan(radians(swhalf))/betav)**2)))
#        CLv = CLv0 + CLvbeta*beta+CLvdeltar*deltar
#        Svi = 0.5*Aircraft.ParAnFP.T_to*Aircraft.ParLayoutConfig.y_engine/(lvi*0.5*rho*Vmc**2*CLv)
#        print(Svi)
    


#    VL = 40  #landing speed !!!!!!!!!
#    Vw = 12.861   #CS25 Mximum crosswind velocity (90degree)
#    betaw = atan(Vw/VL)
#    lac = 2    #distance between the side geometric center and landing center of gravity
#    CLvw = CLv0 + CLvbeta*betaw+CLvdeltar*deltar
#    Lv = 0.5*rho*(VL**2+Vw**2)*Sv*CLv
#    Sside = 150   #side surface area!!!!!!!!
#    CDside = 0.65
#    Fw = 0.5*rho*Vw**2*Sside*CDside
#    cwdif = Lv*lvi-Fw*lac
#    
    bv = sqrt(Svi*Avi)
    crv = 2*Svi/bv/(1+trvi)
    ctv = crv*trvi

    
    anfp = Aircraft.ParAnFP
    Vc = anfp.V_cruise
    Vd = 1.4*Vc   #dive speed
    Kv = 1
    Wvt = Kv*(Svi*10.764)*(3.81*((Svi*10.764)**0.2*(Vd/0.5144)/1000/(cos(swhalf))**0.5)-0.287)*0.4536
    mac_v = ((2./3.) * crv * (1. + ctv + ctv**2.)/(1. + ctv))
    swle = atan(tan(swhalf)+4/Avi*0.5*(1-trvi)/(1+trvi))
   
    
    Aircraft.ParLayoutConfig.Svt = Svi
    Aircraft.ParLayoutConfig.xvt = lvi
    Aircraft.ParLayoutConfig.Avt = Avi
    Aircraft.ParLayoutConfig.trvt = trvi
    Aircraft.ParLayoutConfig.Sweep25vt = swquart
    Aircraft.ParLayoutConfig.Sweep50vt = degrees(swhalf)
    Aircraft.ParLayoutConfig.cr_v = crv
    Aircraft.ParLayoutConfig.ct_v = ctv
    Aircraft.ParLayoutConfig.b_v = bv
    Aircraft.ParLayoutConfig.Wvt = Wvt
    Aircraft.ParLayoutConfig.mac_v = mac_v
    Aircraft.ParLayoutConfig.sweepLEvt = swle
    
    