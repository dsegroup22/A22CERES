# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 14:54:24 2019

@author: menno
"""
import numpy as np


def FusAreas(Aircraft):

    struc = Aircraft.ParStruc
    config = Aircraft.ParLayoutConfig

    
    l_nose=config.l_nose
    l_cabin=config.l_cabin
    l_tail=config.l_tail
    
    h_fuselage=config.h_fuselage
    w_fuselage=config.w_fuselage
    d_fuselage=config.d_fuselage
    d_cockpit=config.d_cockpit
    
    h_APU=config.h_APU
    
    Svt=config.Svt
    
    Ss_nose=np.pi*d_cockpit/4*l_nose #(elliptical) spheriod prolate shape
    Ss_cabin=l_cabin*h_fuselage # elliptical cylinder shape
    Ss_tail=(h_fuselage+h_APU)/2*l_tail #cut off cone shape
    
    S_side=sum([Svt,Ss_nose,Ss_cabin,Ss_tail])
    
    e=np.sqrt(1-(d_cockpit/2/l_nose)**2)

    Sw_nose=np.pi*(d_cockpit/2)**2*(1+l_nose/(d_cockpit/2*e)*np.arcsin(e)) #(elliptical) spheriod prolate shape
    
    h=((h_fuselage-w_fuselage)/(h_fuselage+w_fuselage))**2
    Sw_cabin=np.pi*(h_fuselage+w_fuselage)/2*(1+3*h/(10+np.sqrt(4-3*h)))*l_cabin # elliptical cylinder shape
    
    
    l_fullcone=d_fuselage*l_tail/(d_fuselage-h_APU)
    l_imagcone=l_fullcone-l_tail
    Sw_fullcone=np.pi*d_fuselage/2*np.sqrt(l_fullcone**2-(d_fuselage/2)**2)
    Sw_imagcone=np.pi*h_APU/2*np.sqrt(l_imagcone**2-(h_APU/2)**2)
    Sw_tail=Sw_fullcone-Sw_imagcone #cut off cone shape
    
    S_wet=Sw_nose+Sw_cabin+Sw_tail
    
    
    S_front=w_fuselage*h_fuselage*np.pi/4
    #print (e,Sw_nose,Sw_cabin,Sw_tail)
    return S_side,S_wet,S_front

    
    