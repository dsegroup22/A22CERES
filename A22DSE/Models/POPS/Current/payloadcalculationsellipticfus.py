# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt


def PayloadtankVolume(Aircraft):
    payl=Aircraft.ParPayload
    m_payload=payl.m_payload
    rho_payload=payl.rho_payload
    #outputs Payload tank volume
    #inputs total Payload mass and Payload density

    return m_payload/rho_payload #[m^3]

def PayloadtankLengthEllipse(Aircraft):
    payl=Aircraft.ParPayload
    Layout = Aircraft.ParLayoutConfig
    m_payload=payl.m_payload
    rho_payload=payl.rho_payload
    h_fuselage=Layout.h_fuselage
    w_fuselage=Layout.w_fuselage
    #outputs Payload tank length
    #inputs total Payload mass, Payload density and tank diameter
    V_oblate=4/3*np.pi*(w_fuselage/2)*(h_fuselage/2)**2 # Volume of 2 half oblates [m^3]
    if V_oblate>PayloadtankVolume(Aircraft):
        raise ValueError('to large fuselage dimensions')
    V_cyl=PayloadtankVolume(Aircraft)-V_oblate # Volume of cylindrical part of the tank [m^3]
    l_cyl=V_cyl/(w_fuselage*h_fuselage*np.pi/4) # Length of cylindrical part of the tank [m]
    return l_cyl+h_fuselage #[m]

def PayloadtankMassEllipse(Aircraft):
    payl=Aircraft.ParPayload
    Layout = Aircraft.ParLayoutConfig
    m_payload=payl.m_payload
    rho_payload=payl.rho_payload
    t_tank=payl.t_tank
    rho_tank=payl.rho_alu
    h_fuselage=Layout.h_fuselage
    w_fuselage=Layout.w_fuselage
    #outputs Payload tank weight
    #inputs total Payload mass, Payload density, tank diameter, tank thickness and tank material density
    V_oblate=4/3*np.pi*(w_fuselage/2)*(h_fuselage/2)**2 # Volume of 2 half oblates [m^3]
    if V_oblate>PayloadtankVolume(Aircraft):
        raise ValueError('to large fuselage dimensions')
    V_cyl=PayloadtankVolume(Aircraft)-V_oblate # Volume of cylindrical part of the tank [m^3]
    l_cyl=V_cyl/(w_fuselage*h_fuselage*np.pi/4) # Length of cylindrical part of the tank [m]
    e=np.sqrt(1-(w_fuselage/2/h_fuselage)**2)
    A_oblate=2*np.pi*(h_fuselage/2)**2+np.pi*(w_fuselage/2)**2/e*np.log ((1+e)/(1-e)) # Surface area of 2 half oblates [m^2]
    h=((h_fuselage-w_fuselage)/(h_fuselage+w_fuselage))**2
    
    A_cyl=np.pi*(h_fuselage+w_fuselage)/2*(1+3*h/(10+np.sqrt(4-3*h)))*l_cyl # Surface area of cylindrical part of the tank [m]
    return (A_oblate+A_cyl)*t_tank*rho_tank #[kg]


def PayloadcgEllipse(Aircraft):
    Payload=Aircraft.ParPayload
    Layout=Aircraft.ParLayoutConfig
    l_nose=Layout.l_nose
    l_cabin=Layout.l_cabin
    l_tank=Payload.l_tank
    d_tank=Payload.d_tank
    l_burner=Payload.l_burner
    m_tank=Payload.m_tank
    m_burner=Payload.m_burner
    h_fuselage=Layout.h_fuselage
    #xcg_burner=0.85*Layout.l_fuselage # burner @ 85 % of fuselage
    #xcg_tank=xcg_burner-(l_tank+l_burner)/2 # most aft poossible position: place tank directly ahead of the payload

    xcg_tank=l_nose+l_cabin-(l_tank-h_fuselage)/2 # most aft possible position: cylindrical tank section ennds at end of cylindrical cabin section
    xcg_burner=xcg_tank+(l_tank+l_burner)/2 # placed directly aft of the tank
    x_burner_end=xcg_burner+l_burner/2 # check that the burner does not extend further than the fuselage
    xcg_totalpayload_empty=((xcg_tank*m_tank+xcg_burner*m_burner)/(m_tank+m_burner))
    
    return(xcg_tank,xcg_burner,x_burner_end,xcg_totalpayload_empty)
##diameters=np.arange(1,2.5,0.01)
##weights=np.array([])
##
##for D in diameters:
##    weights=np.append(weights,PayloadtankMass(10000,1121,D,0.003,2700))
##
##plt.plot(diameters,weights)
##plt.show()

