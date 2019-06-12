# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 11:21:38 2019

@author: Nout
"""
import numpy as np
def Engines_placement(Aircraft):
    """
    Description:
        this program gives the x and y engine placement, given the amount 
        of engines. For 2 and 4 engines, location is the same, because 2 engines
        will be podded together. For odd numbered engines, 1 will be placed at
        the tail. For conventions regarding engine groups, see drawing on board.
    INPUT:
        Amount of engines, y_locations of major ribs in wing, xlemac, 
        xlemac_vertical tail
    OUTPUT:
        x_loc engine groups
        y_loc engine groups
    """
    #get shortcuts
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    layout = Aircraft.ParLayoutConfig
    prop = Aircraft.ParProp
    
#=========================get parameters=======================================
    #wing
    Sweep_LE = anfp.Sweep_LE
    c_r = anfp.c_r
    b = anfp.b
    x_LE_root = layout.x_LE_root
    #engine
    l_engine = prop.Engine_length
    psi = prop.psi
    xf_c = prop.xf_c
    h_c = prop.h_c
    #tail
    x_lemac_h  = layout.x_lemach
    y_mac_h = layout.y_MACh
    sweepLEht = layout.sweepLEht
    
    
#===================get positions for different configs========================    
    
    if struc.N_engines == 2 or struc.N_engines == 4:
        layout.y_eng_g2 = 0.35*b/2
        layout.y_eng_g1 = np.nan
        layout.y_eng_g3 = np.nan
        
        #get x and z position for g2
        x_le_eng_g2 = x_LE_root+layout.y_eng_g2*np.tan(Sweep_LE)
        lf_eng = psi*l_engine
        c = c_r*layout.y_eng_g2/b
        
        layout.x_eng_g2 = xf_c*c-lf_eng + x_le_eng_g2
        layout.eng_height_under_wing_g2 = h_c*c
        layout.y_eng_out = layout.y_eng_g2
        
        layout.x_le_eng_g1 = np.nan
        layout.x_le_eng_g3= np.nan
        
    if struc.N_engines == 3 or struc.N_engines == 5:
        layout.y_eng_g2 = 0.35*b/2
        layout.y_eng_g1 = 0.
        layout.y_eng_g3 = np.nan
        
        #get x position for g1
        layout.x_eng_g1 = x_lemac_h -y_mac_h*np.tan(sweepLEht)
        
        #get x and z position for g2
        x_le_eng_g2 = x_LE_root+layout.y_eng_g2*np.tan(Sweep_LE)
        lf_eng = psi*l_engine
        c = c_r*layout.y_eng_g2/b
        
        layout.x_eng_g2 = xf_c*c-lf_eng + x_le_eng_g2
        layout.eng_height_under_wing_g2 = h_c*c
        layout.y_eng_out = layout.y_eng_g2

        layout.x_eng_g3 = np.nan
        
    if struc.N_engines == 6 or struc.N_engines == 8:
        layout.y_eng_g2 = 0.35*b/2
        layout.y_eng_g1 = np.nan
        layout.y_eng_g3 = layout.y_aileron
        
        #get x and z position for g2
        x_le_eng_g2 = x_LE_root+layout.y_eng_g2*np.tan(Sweep_LE)
        lf_eng = psi*l_engine
        c = c_r*layout.y_eng_g2/b
        
        layout.x_eng_g2 = xf_c*c-lf_eng + x_le_eng_g2
        layout.eng_height_under_wing_g2 = h_c*c
        
        #get x and z position for g3
        x_le_eng_g3 = x_LE_root+layout.y_eng_g3*np.tan(Sweep_LE)
        lf_eng = psi*l_engine
        c = c_r*layout.y_eng_g3/b
        
        layout.x_eng_g3 = xf_c*c-lf_eng + x_le_eng_g3
        layout.eng_height_under_wing_g2 = h_c*c
        layout.y_eng_out = layout.y_eng_g3
        
        layout.x_eng_g1 = np.nan
        
    if struc.N_engines == 7:
        layout.y_eng_g2 = 0.35*b/2
        layout.y_eng_g1 = 0.
        layout.y_eng_g3 = layout.y_aileron
    
        
        #get x position for g1
        layout.x_eng_g1 = x_lemac_h -y_mac_h*np.tan(sweepLEht)
        
        #get x and z position for g2
        x_le_eng_g2 = x_LE_root+layout.y_eng_g2*np.tan(Sweep_LE)
        lf_eng = psi*l_engine
        c = c_r*layout.y_eng_g2/b
        
        layout.x_eng_g2 = xf_c*c-lf_eng + x_le_eng_g2
        layout.eng_height_under_wing_g2 = h_c*c
        
        #get x and z position for g3
        x_le_eng_g3 = x_LE_root+layout.y_eng_g3*np.tan(Sweep_LE)
        lf_eng = psi*l_engine
        c = c_r*layout.y_eng_g3/b
        
        layout.x_eng_g3 = xf_c*c-lf_eng + x_le_eng_g3
        layout.eng_height_under_wing_g2 = h_c*c
        layout.y_eng_out = layout.y_eng_g3
   
        

        