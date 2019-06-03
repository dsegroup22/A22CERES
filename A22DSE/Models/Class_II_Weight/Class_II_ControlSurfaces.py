# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:36:02 2019

@author: tomhu
"""

def Class_II_Weight_CS(Aircraft):

#DESCRIPTION:
#           This model is based on Torenbeek(1982) p282-283. it calculates the
#           mass of the nose and main landing gear based on statistics, it is 
#           taken in [lbs], so at the end it needs to be converted to [kg].
#INPUTS: 
#           float MTOW: maximum takeoff weight
#           string Wing_config: type of wing configuration, either low or high
#           float A_main, B_main,C_main etc: scaling factors taken from Toren-
#           beek, everything is for pounds. see p282-283
#OUTPUTS:
#           float W_lg_tot: total weight of landing gears in [kg]
#           float W_lg_main: total weight of tandem landing gears in [kg]
#           float W_lg_nose: total weight of nose landing gear in [kg]
    

    
    #make shortcuts for parameter calling
    cs = Aircraft.ParClassII_CS 
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    
    #define inputs:
    MTOW = struc.MTOW
   
    kcs = cs.kcs
    conv = cs.conv
    
        
# =============================================================================
#                       CALCULATE THE LANDING GEAR WEIGHTS      
# =============================================================================
    W_cs = kcs * MTOW**(2/3)*conv
    
    
    return W_cs