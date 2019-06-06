# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 22:37:03 2019

@author: lujingyi
"""
from math import sqrt
def flightenvelope(Aircraft):
    rho = 0.089
    CLmax = Aircraft.ParAnFP.CLMAX  #!!!!!!!!!!!!!!!!!!
    Vs = sqrt(Aircraft.ParStruc.MTOW/(0.5*rho*CLmax*Aircraft.ParAnFP.S))
    nmax = 2.1+24000/(Aircraft.ParStruc.MTOW*2.205+10000)
    nmin = -0.4*nmax
    Va = Vs*sqrt(nmax)
    Vc = Aircraft.ParAnFP.V_cruise
    Vd = 1.4*Vc
    mug = 2*Aircraft.ParStruc.MTOW*2.205/(Aircraft.ParAnFP.S*10.764)/(rho*0.00194*Aircraft.ParAnFP.MAC*3.281*Aircraft.ParAnFP.C_L_alpha_cruise*32.2)
    Kg = 0.6#88*mug/(5.3+mug)
    #ngmax = 1+Kg*50*Vc*1.944*Aircraft.ParAnFP.C_L_alpha_cruise/(498*Aircraft.ParStruc.MTOW*2.205/(Aircraft.ParAnFP.S*10.764))
    ngmax = 1+0.5*rho*Vc*Kg*Aircraft.ParAnFP.C_L_alpha_slow*15/(Aircraft.ParStruc.MTOW/Aircraft.ParAnFP.S)
    
    return(nmax,Vs,Vd)
    
    
    
