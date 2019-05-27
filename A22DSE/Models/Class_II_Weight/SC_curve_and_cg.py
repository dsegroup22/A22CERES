# -*- coding: utf-8 -*-
"""
Created on Mon May 13 18:54:40 2019

@author: lujingyi
"""
import numpy as np
import matplotlib.pyplot as plt
from math import tan,radians,pi,sqrt


def scplot(Aircraft):
#------------inputs-------------------
    anfp = Aircraft.ParAnFP
    etha = 0.95
    M = anfp.M_cruise
    A = anfp.A   #8.
    Lambda = 20.   #!!!!!!!!!!!!!
    beta = sqrt(1-M**2)
    CLalphaw = 2*pi*A/(2.+ sqrt(4.+(A*beta/etha)**2*(1.+(tan(radians(Lambda))/beta)**2))) #/rad
    bf = 1. #[m] wing span inside the fuselage
    b = anfp.b #[m] total wing span
    Snet = 42 #[m^2] S less the projection of the central wing part inside the fuselage
    S = anfp.S 
    CLalphaAh = CLalphaw*(1+2.15*bf/b)*(Snet/S)+pi/2.*bf**2/S
    
    
    Mh = anfp.M_cruise
    Ah = Aircraft.ParLayoutConfig.Aht       #2
    Lambdah = 0
    betah = sqrt(1-Mh**2)
    CLalphah = 2*pi*Ah/(2.+ sqrt(4.+(Ah*betah/etha)**2*(1.+(tan(radians(Lambdah))/betah)**2))) #/rad
    print(CLalphah)   #0.3
    Sh = 10.
    MAC = 1.5
    lh = 15.  #negative for canard
    xac = 30.
    deda = 0.1
    VhV = 1. #1 for T tail and canard
    CLAh = 1.2
    CLh = -0.8
    Cmac = -0.3
    #-----------parameters-----------------
    margin = 0.05
    
    
    #---------stability curve--------------
    xcg = np.arange(0.,100.,1.)
    ShSs = 1/(CLalphah/CLalphaAh*(1-deda)*lh/MAC*VhV**2)*(xcg-xac+margin)
    
    
    #---------controllability--------------
    ShSc = 1/(CLh/CLAh*lh/MAC*VhV**2)*(xcg+Cmac/CLAh-xac)
    
    
    #------------plot--------------------
    plt.plot(xcg,ShSc,"r-",xcg,ShSs,"g--")
    plt.ylim(0,1)
    plt.xlim(0,50)
    plt.show()


#--------------cg-----------------------
def oecg(Aircraft):
    xoe = 0.25 #25% of the fuselage estimate for wing-mounted engine configuration, in the MAC ref 
    #wing group: wing + engine
    MAC = Aircraft.ParAnFP.MAC
    xwing = 0.25*MAC  #MAC ref
    Wwing = Aircraft.ParStruc.Wing_weight #[kg] !!!!!!!!!!!!!Appended!!!!!!!!!
    y_mac = Aircraft.ParAnFP.b/2*(Aircraft.ParAnFP.c_r+2*Aircraft.ParAnFP.c_t)/3/(Aircraft.ParAnFP.c_r+Aircraft.ParAnFP.c_t)
    xengine = (Aircraft.ParAnFP.b*7/40-y_mac)*tan(Aircraft.ParAnFP.Sweep_LE) #MAC ref
    nengine = 2 #number of engine
    Wengine = Aircraft.ParAnFP.We*nengine #[kg]
    Wwg = Wwing+Wengine
    xwg = (xwing*Wwing+xengine*Wengine)/Wwg
    #print(xengine)
    #fuselage group: fuselage, horizontal tail, vertical tail, nose landing gear, main landing gear
    lf = 24   #[m] fuselage length!!!!!! NOT APPENDED YET!!!!!!!
    xf = 0.42*lf  #[m] fuselage cg location
    Wf = Aircraft.ParStruc.Wf         #[kg]
    xht = 0.25*lf+Aircraft.ParLayoutConfig.xht  #[m]
    Wht = Aircraft.ParLayoutConfig.Wht  #[kg]
    xvt = 0.25*lf+Aircraft.ParLayoutConfig.xvt  #[m]
    Wvt = Aircraft.ParLayoutConfig.Wvt  #[kg]
    xnlg = Aircraft.ParLayoutConfig.lg_x_nose   #[m]
    Wnlg = Aircraft.ParStruc.LG_weight_nose  #[kg]
    xmlg = Aircraft.ParLayoutConfig.lg_x_main  #[m]
    Wmlg = Aircraft.ParStruc.LG_weight_main #[kg]
    Wfg = Wf+Wht+Wvt+Wnlg+Wmlg #[kg]
    xfg = (xf*Wf+xht*Wht+xvt*Wvt+xnlg*Wnlg+xmlg*Wmlg)/Wfg  #[m]
    #print(Wfg,xfg)
#    print(xnlg,Wnlg)
#    xnlg = 5. #Aircraft ref
#    Wnlg =30.  #[N]
#    xfg = 45. #fuselage cg in global reference, measured on the aircraft ref system
#    xwg = 25. #wing group cg, MAC ref
#    Wfg = 10000. #[N]
#    Wwg = 5000. #[N]
    xlemac = xfg-xoe+Wfg/Wwg*(xwg-xoe) #first estimation of the wing position in aircraft ref
    
    return(xlemac,Wfg,xfg)
#    print(xlemac)
#    
#    xlemac = np.arange(0,100,5)
#    xoeit = (xfg+Wwg/Wfg*xwg-xlemac)/(1+Wwg/Wfg)
#    print(xoeit)







