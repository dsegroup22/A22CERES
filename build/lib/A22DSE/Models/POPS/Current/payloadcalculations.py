# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys
sys.path.append('../')


#import parameters

import numpy as np
import matplotlib.pyplot as plt


def InletArea(m_sulphur,airtofuel,t_cruise,M,a_cruise,rho):
    #function that calculates the required inlet area of the burner, using the altitude, sulphur mass, cruise mach number
    #and air to fuel ratio as an input
    
    v=a_cruise*M #cruise speed   
    m_dotS=m_sulphur/t_cruise #mass flow of sulphur [kg/s]
    m_dotair=(airtofuel)*m_dotS #required air mass flow [kg/s]
    m_dottotal=m_dotS+m_dotair
    return m_dottotal/v/rho #required inlet area [m2]


def SulphursMassdisprate(m_sulphur,t_cruise,M_cruise,a_cruise):
    #outputs Sulphur dispersion rate
    #input total sulphur mass, cruise time, cruise Mach number and speed of sound during cruise
    
    v=a_cruise*M_cruise #cruisespeed [m/s]
    return m_sulphur/t_cruise/v #[kg/m]

def BurnerMass(m_sulphur,t_cruise,airtofuel):
    #function that calculates the burner mass, using the sulphur mass, cruise time and air to fuel ratio
    
    m_dotS=m_sulphur/t_cruise #mass flow of sulphur [kg/s]
    m_dotair=airtofuel*m_dotS #required air mass flow [kg/s]
    m_dottotal=m_dotS+m_dotair #total outflow [kg/s]
    
    return 1.6*(304*m_dottotal**0.9)**0.7 # burner mass [kg]

def SulphurtankVolume(m_sulphur,rho_sulphur):
    #outputs sulphur tank volume
    #inputs total sulphur mass and sulphur density

    return m_sulphur/rho_sulphur #[m^3]

def SulphurtankLength(m_sulphur,rho_sulphur,d_tank):
    #outputs sulphur tank length
    #inputs total sulphur mass, sulphur density and tank diameter
    V_sphere=d_tank**3/6*np.pi # Volume of 2 half spheres [m^3]
    if V_sphere>SulphurtankVolume(m_sulphur,rho_sulphur):
        raise ValueError('to large d_tank')
    V_cyl=SulphurtankVolume(m_sulphur,rho_sulphur)-V_sphere # Volume of cylindrical part of the tank [m^3]
    l_cyl=V_cyl/(d_tank**2*np.pi/4) # Length of cylindrical part of the tank [m]
    return l_cyl+d_tank #[m]

def SulphurtankMass(m_sulphur,rho_sulphur,d_tank,t_tank,rho_tank):
    #outputs sulphur tank weight
    #inputs total sulphur mass, sulphur density, tank diameter, tank thickness and tank material density
    V_sphere=d_tank**3/6*np.pi # Volume of 2 half spheres [m^3]
    if V_sphere>SulphurtankVolume(m_sulphur,rho_sulphur):
        raise ValueError('to large d_tank')
    V_cyl=SulphurtankVolume(m_sulphur,rho_sulphur)-V_sphere # Volume of cylindrical part of the tank [m^3]
    l_cyl=V_cyl/(d_tank**2*np.pi/4) # Length of cylindrical part of the tank [m]
    A_sphere=d_tank**2*np.pi # Surface area of 2 half spheres [m^2]
    A_cyl=d_tank*np.pi*l_cyl # Surface area of cylindrical part of the tank [m]
    return (A_sphere+A_cyl)*t_tank*rho_tank #[kg]


##diameters=np.arange(1,2.5,0.01)
##weights=np.array([])
##
##for D in diameters:
##    weights=np.append(weights,SulphurtankMass(10000,1121,D,0.003,2700))
##
##plt.plot(diameters,weights)
##plt.show()

