# -*- coding: utf-8 -*-
"""
Created on Wed May 15 10:34:42 2019

@author: atiqah
"""
import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, pi
import os
from pathlib import Path
import sys


def Airfoil(Aircraft):
    #file = open('NASASC20714.csv')
    os.chdir(Path(__file__).parents[5])
    #sys.path.append('../../../../../../')
    direct = 'A22DSE/Parameters/'
    file = open(direct+'NASASC20712.csv', 'r')
    #file = open('NASASC20614.csv')
    lines = file.readlines()[11:]
    file.close()
    
    aoa = []
    Cl = []
    Cd = []
    Cdp = [] #pressure drag coefficient
    Cm = []
    
    
    for x in lines:
        aoa.append(float(x.split(',')[0]))
        Cl.append(float(x.split(',')[1]))
        Cd.append(float(x.split(',')[2]))
        Cdp.append(float(x.split(',')[3]))
        Cm.append(float(x.split(',')[4]))
       
    cl_alpha = (Cl[119] - Cl[79])/(aoa[119]-aoa[79])
    tc = 0.12
    cl_max = max(Cl)
    Cd_0 = 0.008 #from graph
    cm_0 = -0.123 #from graph
    #print (Clalpha)
    
    
    a = np.polyfit(aoa, Cl, 3)
    #b = np.polyfit(aoa,Cd,2)
    
    #print(z)
    
    clalpha_new = a[0]*np.array(aoa)**3+a[1]*np.array(aoa)**2+a[2]*np.array(aoa)+a[3]
    #cdalpha_new = b[0]*np.array(aoa)**2+b[1]*np.array(aoa)+b[2]
    
    #plt.figure(1)
    #plt.plot(np.array(Cd),np.array(Cl))
    #plt.xlabel('Cd [-]')
    #plt.ylabel('Cl [-]')
    #plt.title('Cl vs Cd')
    #plt.figure(1)
    #plt.plot(np.array(aoa),clalpha_new)
    ##plt.axhline(0,color='r')
    #plt.xlabel('aoa [deg]')
    #plt.ylabel('Cl [-]')
    #plt.title('Cl vs alpha')
    ##plt.figure(2)
    #plt.plot(np.array(aoa),np.array(Cl))
    ##plt.axhline(0,color='r')
    #plt.xlabel('aoa [deg]')
    #plt.ylabel('Cl [-]')
    #plt.title('Cl vs alpha')
    ##plt.figure(3)
    #plt.plot(np.array(aoa),np.array(Cd))
    #plt.xlabel('aoa [-]')
    #plt.ylabel('Cd [-]')
    #plt.figure(4)
    #plt.plot(np.array(aoa),np.array(Cm))
    #plt.xlabel('aoa [deg]')
    #plt.ylabel('Cm [-]')
    #plt.title('Cm vs alpha')
    ##plt.plot(np.array(Cn),np.array(Cl))
    ##plt.xlabel('Cn')
    ##plt.ylabel('Cl')
    #plt.show()
    #os.chdir(Path(__file__).parents[4])
    return cl_alpha, cl_max, tc, Cd_0, cm_0
