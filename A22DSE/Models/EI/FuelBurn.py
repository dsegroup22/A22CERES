# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 10:34:18 2019

@author: tomhu
"""
import numpy as np


def GetFuelBurn(mdot, resolution):
    '''
    INPUT: mass fuel flow, resolution of mass fuel flow measurement (time)
    OUTPUT: Fuel Burned
    DESCRIPTION: numerical integration based on the method of the 
    trapezoidal discrete integral
    '''    
    dt = resolution
    
    fuelburn = np.trapz(mdot, x= None, dx =dt)
    
    return fuelburn

def GetAltitude(altitude, data):
    '''
    INPUT: altitude float, data array
    OUTPUT: selection of data at the right altitude
    '''
    newdata = np.where( np.logical_and(data[:,0] > altitude, data[:,0]\
                       <altitude + 400))
    newdata = data[newdata]
    return newdata

def GetMach(Mach, data):
    '''
    INPUT: Machnumber, data
    OUTPUT: selection of data at right mach number
    '''
    newdata = np.where(np.logical_and(data[:,1] > Mach , data[:,1] \
                                      < Mach + 0.014))
    newdata = data[newdata]
    return newdata
#def GetDataMdot(file):
#    read file
#    get mdot from it 
    

file = open("testfile.txt", "r") 
file = file.readlines()    
heading = file[1]
file = file[4:]

for i in range(len(file)):
    file[i] = file[i].split()
    for j in range(len(file[i])):
        file[i][j] = float(file[i][j])
data = file
data = np.array(data)

def GetEngineProp(altitude, Mach):
    info = GetMach(Mach, GetAltitude(altitude, data))
    return info

a = GetEngineProp(1500,0.8)