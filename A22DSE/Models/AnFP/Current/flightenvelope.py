# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 22:37:03 2019

@author: lujingyi
"""
from math import sqrt
from matplotlib import pyplot as plt
import numpy as np
def flightenvelope(Aircraft):
    rho = 0.089
    rho0 = 1.225
    eas = sqrt(rho/rho0)
    CLmax = Aircraft.ParAnFP.CLMAX  
    Vs = sqrt(Aircraft.ParStruc.MTOW/(0.5*rho*CLmax*Aircraft.ParAnFP.S))
    nmax = 2.1+24000/(Aircraft.ParStruc.MTOW*2.205+10000)
    nmin = -0.4*nmax
    Va = Vs*sqrt(nmax)
    Vg = Vs*sqrt(-nmin)
    Vc = Aircraft.ParAnFP.V_cruise
    Vd = 1.4*Vc
    #mug = 2*Aircraft.ParStruc.MTOW*2.205/(Aircraft.ParAnFP.S*10.764)/(rho*0.00194*Aircraft.ParAnFP.MAC*3.281*Aircraft.ParAnFP.C_L_alpha_cruise*32.2)
    #Kg = 0.7#88*mug/(5.3+mug)
    mug = 2*Aircraft.ParStruc.MTOW/(Aircraft.ParAnFP.S)/(rho*Aircraft.ParAnFP.MAC*Aircraft.ParAnFP.C_L_alpha_cruise*9.80665)
    Kg = 0.88*mug/(5.3+mug)
    #ngmax = 1+Kg*50*Vc*1.944*Aircraft.ParAnFP.C_L_alpha_cruise/(498*Aircraft.ParStruc.MTOW*2.205/(Aircraft.ParAnFP.S*10.764))
    ngmaxc = 1+0.5*rho*Vc*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*15.24/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    ngminc = 1-0.5*rho*Vc*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*15.24/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    ngmaxd = 1+0.5*rho*Vd*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*7.62/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    ngmind = 1-0.5*rho*Vd*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*7.62/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    return(max(ngmaxc,nmax)*1.5,max(ngmaxc,nmax),Vs,Vd)

#    x_mu1 = np.arange(0,Va,1)
#    y_mu1 = x_mu1**2*0.5*rho*CLmax*Aircraft.ParAnFP.S/Aircraft.ParStruc.MTOW
#    x_mu2 = np.arange(Va,Vd,1)
#    y_mu2 = nmax*x_mu2/x_mu2
#    x_ml1 = np.arange(0,Vg,1)
#    y_ml1 = -x_ml1**2*0.5*rho*CLmax*Aircraft.ParAnFP.S/Aircraft.ParStruc.MTOW
#    x_ml2 = np.arange(Vg,Vd,1)
#    y_ml2 = nmin*x_ml2/x_ml2   
#    x_gu1 = np.arange(0,Vc,1)
#    y_gu1 = (ngmaxc-1)/Vc*x_gu1+1
#    x_gu2 = np.arange(Vc,Vd,1)
#    y_gu2 = (ngmaxd-ngmaxc)/(Vd-Vc)*(x_gu2-Vd)+ngmaxd
#    x_gl1 = np.arange(0,Vc,1)
#    y_gl1 = (ngminc-1)/Vc*x_gl1+1
#    x_gl2 = np.arange(Vc,Vd,1)
#    y_gl2 = (ngmind-ngminc)/(Vd-Vc)*(x_gl2-Vd)+ngmind   
#    plt.plot(x_mu1,y_mu1)
#    plt.plot(x_mu2,y_mu2)
#    plt.plot(x_ml1,y_ml1)
#    plt.plot(x_ml2,y_ml2)
#    plt.plot(x_gu1,y_gu1)
#    plt.plot(x_gu2,y_gu2)
#    plt.plot(x_gl1,y_gl1)
#    plt.plot(x_gl2,y_gl2)
#    plt.show()


