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
    Lambda = Aircraft.ParAnFP.Sweep_LE   #!!!!!!!!!!!!!
    beta = sqrt(1-M**2)
    CLalphaw = 0.14*(180/pi) #2*pi*A/(2.+ sqrt(4.+(A*beta/etha)**2*(1.+(tan(radians(Lambda))/beta)**2))) #/rad
    bf = Aircraft.ParLayoutConfig.w_fuselage #[m] wing span inside the fuselage
    b = anfp.b #[m] total wing span
    layoutconfig = Aircraft.ParLayoutConfig
    Snet = anfp.S - anfp.c_r*layoutconfig.w_fuselage #[m^2] S less the projection of the central wing part inside the fuselage
    S = anfp.S 
    CLalphaAh = CLalphaw*(1+2.15*bf/b)*(Snet/S)+pi/2.*bf**2/S
    
    
    Mh = anfp.M_cruise
    Ah = Aircraft.ParLayoutConfig.Aht       #2
    Lambdah = Aircraft.ParLayoutConfig.sweepLEht
    betah = sqrt(1-Mh**2)
    CLalphah = 2*pi*Ah/(2.+ sqrt(4.+(Ah*betah/etha)**2*(1.+(tan(radians(Lambdah))/betah)**2))) #/rad  #0.3
    #Sh = Aircraft.ParLayoutConfig.Sht #10
    MAC = Aircraft.ParAnFP.MAC
    lh = Aircraft.ParLayoutConfig.xht  #negative for canard
    xac = 0.25*MAC+Aircraft.ParLayoutConfig.x_lemac #30.
    deda =  0.1 #(0.006 from horizontaltail calculation)
    VhV = 1. #1 for T tail and canard
    CLAh = 1
    CLh = -0.8
    Cmac = -0.3
    #-----------parameters-----------------
    margin = 0.05
    
    
    #---------stability curve--------------
    xcg = np.arange(0.,100.,1.)
    ShSs = 1/(CLalphah/CLalphaAh*(1-deda)*lh/MAC*VhV**2)*(xcg-xac+margin)
    
    xcg_mac = (xcg-Aircraft.ParLayoutConfig.x_lemac)/MAC
    #---------controllability--------------
    ShSc = 1/(CLh/CLAh*lh/MAC*VhV**2)*(xcg+Cmac/CLAh-xac)
#    
#    a = np.polyfit(xcg_mac,ShSs,1)
#    b = np.polyfit(xcg_mac,ShSc,1)
    
#    solve1 = np.array([[1,-a[0],0],[1,0,-b[0]],[0,1,-1]])
#    solve2=np.array([a[1],b[1],0.59])
#    x = np.linalg.solve(solve1, solve2)
    #------------plot--------------------
    plt.plot(xcg_mac,ShSc,"r-",xcg_mac,ShSs,"g--")
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.ylabel('Sh/S')
    plt.xlabel('xcg/MAC')
    plt.title('Scissor Plot')
    plt.savefig('SCPlot.png')
    plt.show()
    


#--------------cg-----------------------
def oecg(Aircraft):
    xcg_totalpayload_empty_aft = Aircraft.ParPayload.xcg_totalpayload_empty
    xcg_totalpayload_empty_fwd = Aircraft.ParPayload.xcg_totalpayload_empty_fwd
    payload_empty = np.arange(int(xcg_totalpayload_empty_fwd), int(xcg_totalpayload_empty_aft),1)
    #-------------------------
    xoe = 0.25 #25% MAC estimate for wing-mounted engine configuration, in the MAC ref 
    #wing group: wing + engine
    MAC = Aircraft.ParAnFP.MAC
    xwing = 0.25*MAC  #MAC ref
    Wwing = Aircraft.ParStruc.Wing_weight #[kg] !!!!!!!!!!!!!Appended!!!!!!!!!
    y_mac = Aircraft.ParAnFP.b/2*(Aircraft.ParAnFP.c_r+2*Aircraft.ParAnFP.c_t)/3/(Aircraft.ParAnFP.c_r+Aircraft.ParAnFP.c_t)
    xengine = (Aircraft.ParAnFP.b*7/40-y_mac)*tan(Aircraft.ParAnFP.Sweep_LE) #MAC ref
    nengine = Aircraft.ParStruc.N_engines #number of engine
    Aircraft.ParProp.Engine_weight_Total = Aircraft.ParProp.Engine_weight*nengine #[kg]
    Wengine =  Aircraft.ParProp.Engine_weight_Total
    Wwg = Wwing+Wengine
    xwg = (xwing*Wwing+xengine*Wengine)/Wwg #percentage of MAC so from lemac
    #print(xwg)
    #fuselage group: fuselage, horizontal tail, vertical tail, nose landing gear, main landing gear
    lf = Aircraft.ParLayoutConfig.l_fuselage #max(Aircraft.ParLayoutConfig.xvt, Aircraft.ParLayoutConfig.xht) + Aircraft.ParLayoutConfig.l_nose  #[m] fuselage length!!!!!! NOT APPENDED YET!!!!!!!
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
    Wpl = Aircraft.ParPayload.m_tank + Aircraft.ParPayload.m_burner # [kg] payload tank + burner 
    xpl = 7.35 #18 #Aircraft.ParPayload.xcg_totalpayload_empty #DUMMY VALUE!
    Wfg = Wf+Wht+Wvt+Wnlg+Wmlg #[kg]
    xfg = (xf*Wf+xht*Wht+xvt*Wvt+xnlg*Wnlg+xmlg*Wmlg+Wpl*xpl)/Wfg  #[m]
    #print (xfg)
    #print(Wfg,xfg)
#    print(xnlg,Wnlg)
#    xnlg = 5. #Aircraft ref
#    Wnlg =30.  #[N]
#    xfg = 45. #fuselage cg in global reference, measured on the aircraft ref system
#    xwg = 25. #wing group cg, MAC ref
#    Wfg = 10000. #[N]
#    Wwg = 5000. #[N]
    xlemac = xfg-xoe+Wfg/Wwg*(xwg-xoe) #first estimation of the wing position in aircraft ref
#     #-----------------------loading diagram
#     
##    xcg_totalpayload_empty_aft = Aircraft.ParPayload.xcg_totalpayload_empty
##    xcg_totalpayload_empty_fwd = Aircraft.ParPayload.xcg_totalpayload_empty_fwd
#    rangecg = np.array([0.9,1,1.1])
#    xcg_fwd = []
#    xcg_aft = []
#    y = []
#    
#    for i in range(len(rangecg)):
#        MAC = Aircraft.ParAnFP.MAC
#        lh = Aircraft.ParLayoutConfig.xht
#          
#        #xpayload = np.array([0.8,0.7,0.6,0.5,0.4,0.3,0.2]*l_fuselage)
#        xcg_totalpayload_empty = xpl #17 #Aircraft.ParPayload.xcg_totalpayload_empty
#        #print (xcg_totalpayload_empty)
#        
#        fuel_mass = Aircraft.ParStruc.FW
#        payload_mass = Aircraft.ParPayload.m_payload #13500 #append value [kg]
#        
#        x_lemac = Aircraft.ParLayoutConfig.x_lemac*rangecg[i]
#        
#        oew = Aircraft.ParStruc.OEW
#        x_oew = Aircraft.ParLayoutConfig.x_oe*MAC + x_lemac
#        
#        top = x_oew*oew #append real value
#        bottom = oew #kg append real value
#        payload_mlist = np.ones(int(payload_mass))
#        
#        cg_range = [x_oew]
#        wrange = [oew]
#        
#        xfuel = 0.5*MAC+x_lemac #assumptions
#        fuel_mlist = np.ones(int(fuel_mass))
#        
#        for i in range(int(fuel_mass)):
#            cg = (top + xfuel*fuel_mlist[i])/(bottom + fuel_mlist[i])
#            top = (top + xfuel*fuel_mlist[i])
#            bottom = bottom + fuel_mlist[i]
#            cg_range.append(cg)
#            wrange.append(bottom)
#            
#        fuelindex = len(cg_range)
#        
#        #xf must be changed to the loading of the sulphur
#        #loading for payload
#        for i in range(int(payload_mass)):
#            cg = ((top + xcg_totalpayload_empty*payload_mlist[i]))/(bottom + payload_mlist[i])
#            top = (top + xcg_totalpayload_empty*payload_mlist[i])
#            bottom = bottom + payload_mlist[i]
#            cg_range.append(cg)
#            wrange.append(bottom)
#     
#        #loading for fuel
#    #    for i in range(fuel_mass):
#            
#        cg_range_mac = (cg_range-x_lemac)/MAC
#        x_oew_mac = Aircraft.ParLayoutConfig.x_oe / MAC
#        
#        xcg_fwd.append(min(cg_range_mac))
#        xcg_aft.append(max(cg_range_mac))
#        
#        l_fuselage = Aircraft.ParLayoutConfig.l_fuselage
#        y.append(x_lemac/l_fuselage)
#        
#        
#        #plt.plot((cg_range-x_lemac)/MAC,wrange)
##        plt.plot(cg_range_mac[0:fuelindex+1],np.array(wrange[0:fuelindex+1]),color='palevioletred',label='Fuel')
##        plt.plot(cg_range_mac[fuelindex:],np.array(wrange[fuelindex:]),color='plum', label='Payload')
##        plt.legend(loc=1)
##        plt.axvline(x=max(cg_range_mac), color='gray', linestyle='--')
##        plt.axvline(x=min(cg_range_mac), color='gray', linestyle='--')
##        plt.axvline(x=max(cg_range_mac)+0.02, color='indianred', linestyle='--')
##        plt.axvline(x=min(cg_range_mac)-0.02, color='indianred', linestyle='--')
##        plt.annotate('OEW',(x_oew_mac,oew))
##        plt.show()
#        
#    plt.plot(xcg_fwd,y)
#    plt.plot(xcg_aft,y)
#    plt.ylabel('xcg/l_fuselage')
#    plt.xlabel('xcg/MAC')
#    plt.title('Loading diagram')
#    plt.xlim(0,1)
#    plt.show()
    
    return(xlemac,Wfg,Wwg,xfg)
#    print(xlemac)
#    
#    xlemac = np.arange(0,100,5)
#    xoeit = (xfg+Wwg/Wfg*xwg-xlemac)/(1+Wwg/Wfg)
#    print(xoeit)

def xoe(Aircraft):
    x_oe = 0.25
    return(x_oe)





