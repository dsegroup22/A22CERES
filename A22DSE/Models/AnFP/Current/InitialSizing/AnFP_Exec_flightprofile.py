# -*- coding: utf-8 -*-
"""
Created on Tue May  7 12:32:12 2019

@author: Atiqah
"""

from math import cos, sin, tan, sqrt, pi, e
import matplotlib.pyplot as plt
import numpy as np
import sys
sys.path.append('../../../../../')
#from A22DSE.Parameters.Par_Class_Atmos import Atmos
#import A22DSE.Parameters.Par_Class_Diff_Configs as Aircraft
from A22DSE.Models.POPS.Current.cruisecalculations import CruiseRange

def Lowbypassafter(height, Fsl, ISA_model,M):
    Tamb, Pamb = ISA_model.ISAFunc([height])[0:2] #Calculation of ambient conditions
    theta0 = Tamb/288.15*(1+0.4/2*M**2) #Calculation of total temp relative with 1D compressibility
    delta0 = Pamb/101325*(1+0.4/2*M**2)**(1.4/0.4) #Calculation of total temp relative with 1D compressibility
    TR = 1.0 #Throttle ratio
    if theta0 <= TR:
        F = Fsl*delta0 #Empirical formula "General Aviation Aircraft Design, Applied Methods and Procedures" page 200
    else:
        F = Fsl*delta0*(1-3.5*(theta0-TR)/(theta0))
    return F

def FuelFractions(Aeroplane,atmosphere):
##    atmosphere = Atmos()
    anfp = Aeroplane.ParAnFP
    m_payload = Aeroplane.ParPayload.m_payload
    dispersionrate = Aeroplane.ParPayload.dispersionrate
    dt = 5 #[s] time increment

    #atmospheric properties during take-off
    g = atmosphere.g0 #par.get('g_0') #[m/s2] #gravitational acceleration at sea-level
    rho0 = atmosphere.rho0 #[kg/m3] #density at sea level


    ########## My Values

    WS0 = Aeroplane.ParAnFP.WS
    TW0 = Aeroplane.ParAnFP.TtoW
    SFC = Aeroplane.ParAnFP.SFC

    CD0 = Aeroplane.ParAnFP.CD0 #at take-off (ground run) <subject to change>
    A = Aeroplane.ParAnFP.A #aspect ratio <subject to change>
    e = Aeroplane.ParAnFP.e #Oswald's efficiency factor <subject to change>

    haccel = 10000/3.28
    hcruise = Aeroplane.ParAnFP.h_cruise
    s_cruise = anfp.s_cruise
    rdump = s_cruise + Aeroplane.ParAnFP.Extrarange
    Mdd = Aeroplane.ParAnFP.Mdd


    deltav = 0.0001




    def RCV(WS0,TW0,CD0,A,e,v,rho,g,dvdh):
        #INPUT: Wing loading, Thrust Loading, CD0, aspect ratio, oswald factor, density, velocity, gravity constant and velocity change per height change
        #OUTPUT: Rate of climb
        CL = 2*WS0/(rho*v**2)
        return (TW0-(CD0+CL**2/(np.pi*A*e))*0.5*rho*v**2/WS0)*v/(1+v/g*dvdh)

    def optRCV(WS0,TW0,CD0,A,e,rho,g,deltav):
        v = 10
        def deltarcvdeltav(WS0,TW0,CD0,A,e,rho,v,g,deltav):
            return (RCV(WS0,TW0,CD0,A,e,v+deltav/2,rho,g,0)-RCV(WS0,TW0,CD0,A,e,v-deltav/2,rho,g,0))/deltav
        deltarate = deltarcvdeltav(WS0,TW0,CD0,A,e,rho,v,g,deltav)
        while deltarate > 10**-12:
            deltarate = deltarcvdeltav(WS0,TW0,CD0,A,e,rho,v,g,deltav)
            deltasquared = (deltarcvdeltav(WS0,TW0,CD0,A,e,rho,v+deltav/2,g,deltav)-deltarcvdeltav(WS0,TW0,CD0,A,e,rho,v-deltav/2,g,deltav))/deltav
            v = v - deltarate/deltasquared
        rate = RCV(WS0,TW0,CD0,A,e,v,rho,g,0)
        return v, rate


    h = np.array([0])
    t = np.array([0])
    d = np.array([0])
    v = 0
    vspeed = np.array([250*0.5144])

    WS = WS0
    TW = TW0
    wfratio = 1
    mf = 0
    dvdh = 0

    while h[-1] < haccel:
        T, press, rho = atmosphere.ISAFunc([h[-1]])
        WS = WS0*(0.99*0.99*0.995*wfratio)
        TW = TW0/(0.99*0.99*0.995*wfratio)*Lowbypassafter(h[-1], 1, atmosphere, v/np.sqrt(1.4*287.05*T))

        v,RCs = optRCV(WS,TW,CD0,A,e,rho,g,deltav)
        if v > 250*0.5144:
            v = 250*0.5144
            RCs = RCV(WS,TW,CD0,A,e,v,rho,g,dvdh)
        else:
            RCs = RCV(WS,TW,CD0,A,e,v,rho,g,dvdh)
    ##    vspread = np.linspace(v-20, v+20, 50)
    ##    ratetest = RCV(WS,TW,CD0,A,e,vspread,rho,g,0)
    ##    plt.plot(vspread,ratetest)
    ##    plt.plot([v,v],[0,RCs])
    ##    plt.pause(0.02)
    ##    plt.clf()    
        h = np.append(h, h[-1]+RCs*dt)
        d = np.append(d, d[-1]+v*dt)
        t = np.append(t, t[-1]+dt)
        vspeed = np.append(vspeed, v)
        mf += (SFC*TW*wfratio*dt)
        wfratio = 1-mf
        dvdh = (vspeed[-1]-vspeed[-2])/(h[-1]-h[-2])
    ##    plt.plot(t,h)
    ##    plt.plot(t,vspeed*10)
    ##    plt.pause(0.02)
    ##    plt.clf()
    ##    print(RCs)

    while h[-1] < hcruise:
        
        T, press, rho = atmosphere.ISAFunc([h[-1]])
        WS = WS0*(0.99*0.99*0.995*wfratio)
        TW = TW0/(0.99*0.99*0.995*wfratio)*Lowbypassafter(h[-1], 1, atmosphere, v/np.sqrt(1.4*287.05*T))
        v,RCs = optRCV(WS,TW,CD0,A,e,rho,g,deltav)
        if v > Mdd*np.sqrt(1.4*287.05*T):
            v = Mdd*np.sqrt(1.4*287.05*T)
            RCs = RCV(WS,TW,CD0,A,e,v,rho,g,dvdh)
        else:
            RCs = RCV(WS,TW,CD0,A,e,v,rho,g,dvdh)
    ##    vspread = np.linspace(v-20, v+20, 50)
    ##    ratetest = RCV(WS,TW,CD0,A,e,vspread,rho,g,0)
    ##    plt.plot(vspread,ratetest)
    ##    plt.plot([v,v],[0,RCs])
    ##    plt.pause(0.02)
    ##    plt.clf()    
        h = np.append(h, h[-1]+RCs*dt)
        d = np.append(d, d[-1]+v*dt)
        t = np.append(t, t[-1]+dt)
        vspeed = np.append(vspeed, v)
        mf += (SFC*TW*wfratio*dt)
        wfratio = 1-mf
        dvdh = (vspeed[-1]-vspeed[-2])/(h[-1]-h[-2])
#        plt.plot(t,h)
#        plt.plot(t,vspeed*10)
#        plt.pause(0.02)
#        plt.clf()
    ##    if (h[-1]-h[-2]) < 0.1:
    ##        break
    dstart = d[-1]
    wfclimb = wfratio

    T, press, rho = atmosphere.ISAFunc([h[-1]])
    while d[-1]-dstart < rdump:
        
        WS = WS0*(0.99*0.99*0.995*wfratio)
        TWmax = TW0/(0.99*0.99*0.995*wfratio)*Lowbypassafter(h[-1], 1, atmosphere, v/np.sqrt(1.4*287.05*T))
        RCs = 0
        CL = np.sqrt(CD0*np.pi*A*e/3)
        v = np.sqrt(2*WS/(rho*CL))
        if v > Mdd*np.sqrt(1.4*287.05*T):
            v = Mdd*np.sqrt(1.4*287.05*T)
            CL = WS/(0.5*rho*v**2)
            CD = (CD0+CL**2/(np.pi*A*e))
            TW = CD/CL
        else:
            CD = (CD0+CL**2/(np.pi*A*e))
            TW = CD/CL
        h = np.append(h, h[-1]+RCs*dt)
        d = np.append(d, d[-1]+v*dt)
        t = np.append(t, t[-1]+dt)
        vspeed = np.append(vspeed, v)
        mf += (SFC*TW*wfratio*dt)
        wfratio = 1-mf
    ##    plt.plot(t,h)
    ##    plt.plot(t,vspeed*10)
    ##    plt.pause(0.005)
    ##    plt.clf()
    ##    

    wfcruise = wfratio
    dfinal = d[-1]
    tfinal = t[-1]
    return wfclimb,wfcruise, dfinal, tfinal
    
    
    
#print(FuelFractions(Aircraft.Conv,Aircraft.ISA_model))


