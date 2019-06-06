# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:07:41 2019

@author: Nout
"""

def Class_II_Weight_LG(Aircraft):

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
    lg = Aircraft.ParClassII_LG 
    anfp = Aircraft.ParAnFP
    struc = Aircraft.ParStruc
    
    #define inputs:
    MTOW = struc.MTOW
    A_main =  lg.A_main
    B_main = lg.B_main
    C_main = lg.C_main
    D_main = lg.D_main
    
    A_nose =  lg.A_nose
    B_nose = lg.B_nose
    C_nose = lg.C_nose
    D_nose = lg.D_nose
    
    #define k_uc, is dependend on wing configuration
    if(anfp.Wing_config == 'low'):
        k_uc = lg.kuc_low_wing
    if(anfp.Wing_config == 'high'):
        k_uc = lg.kuc_high_wing
        
# =============================================================================
#                       CALCULATE THE LANDING GEAR WEIGHTS      
# =============================================================================
    
    W_lg_nose = k_uc*(A_nose+B_nose*MTOW**0.75+C_nose*MTOW+D_nose*MTOW**1.5) #[lbs]
    #Convert into kg
    W_lg_nose = W_lg_nose*Aircraft.ConversTool.lbs2kg #[kg]
    
    W_lg_main = k_uc*(A_main+B_main*MTOW**0.75+C_main*MTOW+D_main*MTOW**1.5) #[lbs]
    #convert into kg
    W_lg_main = W_lg_main*Aircraft.ConversTool.lbs2kg #[kg]
    
    #total lg weight
    W_lg_tot = W_lg_nose+W_lg_main
    
    return W_lg_tot, W_lg_nose,W_lg_main 