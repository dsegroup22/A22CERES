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
    mug = 2*Aircraft.ParStruc.MTOW/(Aircraft.ParAnFP.S)/(rho*Aircraft.ParAnFP.MAC*Aircraft.ParAnFP.C_L_alpha_cruise*9.80665)
    Kg = 0.88*mug/(5.3+mug)

    ngmaxc = 1+0.5*rho*Vc*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*15.24/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    ngminc = 1-0.5*rho*Vc*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*15.24/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    ngmaxd = 1+0.5*rho*Vd*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*7.62/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    ngmind = 1-0.5*rho*Vd*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*7.62/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    return(max(ngmaxc,nmax)*1.5,max(ngmaxc,nmax),Vs,Vd)
    
#    ngmaxc = 1+0.5*rho*Vc*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*15.24/(Aircraft.ParStruc.MTOW*0.63/Aircraft.ParAnFP.S)
#    ngminc = 1-0.5*rho*Vc*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*15.24/(Aircraft.ParStruc.MTOW*0.63/Aircraft.ParAnFP.S)
#    ngmaxd = 1+0.5*rho*Vd*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*7.62/(Aircraft.ParStruc.MTOW*0.63/Aircraft.ParAnFP.S)
#    ngmind = 1-0.5*rho*Vd*eas*Kg*Aircraft.ParAnFP.C_L_alpha_cruise*7.62/(Aircraft.ParStruc.MTOW*0.63/Aircraft.ParAnFP.S)
#
#    print(ngmaxc,nmax,nmin,ngmaxc*1.5,Vs,Va,Vc,Vd)
    
#====================Plot==============================================    
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
#    x_gu3 = np.arange(0,Vd,1)
#    y_gu3 = (ngmaxd-1)/Vd*x_gu3+1
#    x_gl3 = np.arange(0,Vd,1)
#    y_gl3 = (ngmind-1)/Vd*x_gl3+1
#    plt.plot(x_mu1,y_mu1,'r',label='manoeuver limits')
#    plt.plot(x_mu2,y_mu2,'r')
#    plt.plot(x_ml1,y_ml1,'r')
#    plt.plot(x_ml2,y_ml2,'r')
#    plt.plot(x_gu1,y_gu1,'g',label='gust limits')
#    plt.plot(x_gu2,y_gu2,'g')
#    plt.plot(x_gl1,y_gl1,'g')
#    plt.plot(x_gl2,y_gl2,'g')
#    plt.plot(x_gu3,y_gu3,'g')
#    plt.plot(x_gl3,y_gl3,'g')
#    plt.legend(loc=4,fontsize=15)
#    plt.xlim(0,300)
#    plt.ylim(-2,3)
#    plt.scatter(Vs,1)
#    plt.annotate('$V_{stall}$',xy=(Vs+2,0.05),fontsize=15)
#    plt.scatter(Va,nmax)
#    plt.annotate('$V_{A}$',xy=(Va,0.05),fontsize=15)
#    plt.scatter(Vc,ngmaxc)
#    plt.annotate('$V_{C}$',xy=(Vc,0.05),fontsize=15)
#    plt.scatter(Vd,ngmaxd)
#    plt.annotate('$V_{D}$',xy=(Vd,0.05),fontsize=15)
#    plt.axvline(x=Vd,ymin=(nmin+2)/5,ymax=(nmax+2)/5,color='r')
#    plt.axvline(x=Vd,ymin=(ngmind+2)/5,ymax=(ngmaxd+2)/5,color='g')
#    plt.axvline(x=Vs,ymin=2/5,ymax=3/5,color='black',linestyle='dashed')
#    plt.axvline(x=Va,ymax=(nmax+2)/5,ymin=2/5,color='black',linestyle='dashed')
#    plt.axvline(x=Vc,ymax=(ngmaxc+2)/5,ymin=2/5,color='black',linestyle='dashed')
#    plt.axvline(x=Vd,ymax=(ngmaxd+2)/5,ymin=2/5,color='black',linestyle='dashed')
#    plt.axhline(y=1,linewidth=1,color='black')
#    plt.axhline(y=0,linewidth=1,color='black')
#    plt.axhline(y=ngmaxc,xmax=Vc/300,linewidth=1,color='black',linestyle='dashed')
#    plt.axhline(y=nmin,xmax=Vs/300,linewidth=1,color='black',linestyle='dashed')
#    plt.annotate('$n_{max}$',xy=(0,ngmaxc+0.05),fontsize=15)
#    plt.annotate('$n_{min}$',xy=(0,nmin+0.05),fontsize=15)
#    plt.xlabel('Velocity [m/s]',fontsize=15)
#    plt.ylabel('Load Factor',fontsize=15)
#    plt.tick_params(labelsize=15)
#    plt.show()


