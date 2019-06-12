# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:13:22 2019

@author: Nout
"""
import numpy as np

def GetMaxLiftHorTail(Aircraft):
    """
    DESCRIPTION:
        This code calculates maximum load of the horizontal tail on the aircraft,
        it is the summation of the downforce of the tail plus the weight of the
        tail. This is the scenario for take-off.
    INPUTS:
        inputs are the conditions at sealevel, plus the tail weight
    OUTPUTS:
        float F_max_htail = max load of the tail in [N]
    """
    #get shortcuts
    anfp= Aircraft.ParAnFP
    layout = Aircraft.ParLayoutConfig
    
    #get parameters
    clmax_h = -0.8
    rho_SL = anfp.rho_SL
    v_max_to =  anfp.V_max_TO
    S = anfp.S
    
    #calculate forces
    L_max_htail = 0.5*clmax_h*rho_SL*v_max_to**2*S #[N] downforce due to tail
    W_max_htail = (layout.Wht+layout.Wvt)*9.80665 #[N] weight of the total tail
    F_max_htail = L_max_htail+W_max_htail #[N] total Force
    
    return F_max_htail

def NormalStress(Aircraft, x_from_tail, d):
    """
    DESCRIPTION:
        calculates normal stress in crossection, given an location from the tail,
        and the diameter of the cone at a given point.
    INPUTS:     
        location from tail, diameter of cone at location, max tail load
    OUTPUT:
        minimum skin thickness due to normal stress[m]
    """
    #get shortcuts
    struc= Aircraft.ParStruc
   
    #get parameters
    FoS = 1.5 #safety factor
    max_normal_stress = struc.max_yield_stress #[Pa] yield stress
    y = d/2 #[m] location of centriod
    F_max_htail = GetMaxLiftHorTail(Aircraft)
    
    #functions
    Moment = F_max_htail*x_from_tail
    t_skin_norm = abs(FoS*Moment*y/(np.pi*(d/2)**3*max_normal_stress))
    
    return t_skin_norm

def MinimumThickness(Aircraft,Xsteps):
    """
    DESCRIPTION:
        this function checks what the minimum thickness is, and where
    INPUT:
        resolution steps
    OUTPUT:
        minimum thickness for the whole cone part of fuselage
    """
    #get shortcut
    layout = Aircraft.ParLayoutConfig
    
    #get parameters
    d_begin = layout.d_fuselage
    d_end = layout.d_end_fus
    x_cabin_end = layout.l_nose+layout.l_cabin
    l_fuselage = layout.l_fuselage
    
    #geometric functions
    t_skin = []
    x_cone = np.linspace(x_cabin_end,l_fuselage,Xsteps) #xlocations of cone
    x_cone_local = x_cone-x_cabin_end*np.ones(len(x_cone)) #local coordinates
    x_from_tail = x_cone_local[::-1]
    d_cone = d_begin-d_end/d_begin*x_cone_local #diameter of cone at given xlocation
    
    #get t_skin for every step within cone
    for i in range(0,Xsteps):
        t_skin.append( NormalStress(Aircraft,x_from_tail[i], d_cone[i]))
        
    return max(t_skin)
        
        
    
    
    
    
    
test = True

if test:
    import os
    from pathlib import Path
    os.chdir(Path(__file__).parents[5])
    from A22DSE.Parameters.Par_Class_Conventional import Conv

