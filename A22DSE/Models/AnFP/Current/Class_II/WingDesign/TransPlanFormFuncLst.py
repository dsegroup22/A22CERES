# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 02:06:46 2019

@author: hksam
"""

import numpy as np
import os
from pathlib import Path
os.chdir(Path(__file__).parents[6])


import A22DSE.Models.AnFP.Current.\
       Class_II.WingDesign.FunctionsPlanform as GenFunc
# =============================================================================
#               FUNCTIONS FOR TRANSONIC WING PLANFORM DESIGN
# =============================================================================

'''
ASSUMPTIONS:
    - muT = 0.25 (check muT func)
    - rh  = 0.10
    - omegaS = 210 N/m²
    - e_curl = 0.80
    - shape_factor = 3.0    (2.5 < x < 3.5)
    - d_(w+h) = 1.25        (total wing profile drag)
    - CDc = 0.0010
    - M* = 0.935           (2nd gen supercritical airfoils)
'''


def OverallEff(Aircraft, ISA_model, TSFC):
    '''
    INPUT: ISA model, TSFC in kg/h/N
    OUTPUT: OEF; Overall efficiency, i.e. (Thrust Power) / (Rate of Fuel added)
    DESCRIPTION:
    '''
    
    # from GasTurb: M = 0.73; TSFC = 0.061243 kg/h/N => 0.28444
    
    h_cruise = Aircraft.ParAnFP.h_cruise
    V_cruise = Aircraft.ParAnFP.V_cruise

    M_sl, a_sl = ISA_model.GiveMeMach(0, V_cruise)
    M_h, a_h   = ISA_model.GiveMeMach(h_cruise, V_cruise)    
    T, P, rho = ISA_model.ISAFunc([h_cruise])    

    T_rel = T/ISA_model.T0
    
#    print(a_sl, Hg, M_h, T_rel, TSFC)
#    return a_sl/Hg*M_h*np.sqrt(T_rel)/TSFC
    return 0.0287*M_h/TSFC*np.sqrt(T_rel)

def CoPLatCoor(Aircraft):
    return 0.36*(1+Aircraft.ParAnFP.taper)**0.5

def ComputemuT(Aircraft):
    '''
    INPUT: 
    OUTPUT: powerplant weight per unit T_TO
    DESCRIPTION: W_nac is around 1% of MTOW according to parametric study;
    for contingency we'll use 1.5%
    '''
    #todo: change np.min to np.MAX
    
    #ASSUMPTIONS AND CONSTANTS
    T_TO = Aircraft.ParAnFP.T_to
    N_engine = T_TO/60000.
    
    #Determining Engine Weight
    W_engineSheet = Aircraft.ParProp.Engine_weight*9.81*N_engine
    W_engineStat  = 0.25 * T_TO

    Wpp           = np.min([W_engineSheet,W_engineStat])
    
    return Wpp / T_TO


def ComputeTheta2(Aircraft, ISA_model):
    '''INPUT:
       OUTPUT: returns dimless. quasi-analytical parameter for transonic
       planform sizing
       DESCRIPTION: Returns theta_2 which is a dimensionless quasi-analytical
       parameter used in equation to optimise for transonic and subsonic wing
       planforms in terms of (t/c), AR, sweep, and CL.
    '''
    
    #TODO: compute omegaS for composite wing
    
    rh = 0.10                                   # typical value REF Torenbeek
    q_des = GenFunc.DynamicPressEq(Aircraft, ISA_model)
    omegaS = 290  # N/m² for ALUMINIUM WING
                  # Composite wing betw. 34% -  40% lighter than aluminium one
                  
    return (1+rh)*omegaS/q_des/10

def ComputeTheta3(Aircraft, ISA_model):
    '''INPUT:
       OUTPUT: returns dimless. quasi-analytical parameter for transonic
       planform sizing
       DESCRIPTION: Returns theta_3, which replaces theta_1 in the design of 
       transonic planform design. As a result, two additional selection
       variables can be used. Namely, (t/c) and the sweep angle of the wing.
    '''
    
    #TODO: rh is approx. 0.10; CHANGE when Class II weights are set up.
    
    # CONSTANTS AND ASSUMPTIONS
    rh = 0.10                                                # typical value
    WfuMTOW = Aircraft.ParStruc.wfratio
    fuelused = WfuMTOW*Aircraft.ParStruc.MTOW
    MZFW = (Aircraft.ParStruc.MTOW - fuelused)*ISA_model.g0
    bref = 100 #constant in analytical eq.         
    
    
    eta_cp = CoPLatCoor(Aircraft)                            # pg.236 Torenbeek
    n_ult = Aircraft.ParAnFP.n_ult
    q_eq = GenFunc.DynamicPressEq(Aircraft, ISA_model)
    
    
    return 0.0013*(1+rh)*eta_cp*n_ult*np.sqrt(MZFW/q_eq)/bref

def Compute_tc_limit(Aircraft, CL, sweep):
    '''
    DESCRIPTION: !!!NOTE!!! NOT t/c itself! divide this value by cos(sweep)**2,
    i.e.: it returns t/c * cos(sweep_w)**2
    '''
    # Constants
    Mcrit = 0.935
    Mdd = Aircraft.ParAnFP.Mdd
    
    tc_limit = (np.cos(sweep)**3*(Mcrit - Mdd * np.cos(sweep)) - 
            0.1*1.1**1.5 * CL**1.5)
    
    return tc_limit

def ComputeCDpCurl(Aircraft, CL, sweep):
    '''
    INPUT: Aircraft, average t/c_w [-], sweep in [rad]
    OUTPUT: profile drag of the wing
    '''
    
    def ComputeRe():
        '''
        Computes the experienced Re of the chord
        '''
        if np.abs((Aircraft.ParAnFP.h_cruise-20000)/20000) < 0.05:
            v = 0.0000143226
        else:
            ValueError("Not programmed yet\n")
        u = Aircraft.ParAnFP.V_cruise
        L = Aircraft.ParAnFP.MAC
        return u*L/v

    def SkinFrict(Mcruise, Re):
        Cfi = 0.455/(np.power(np.log10(Re), 2.58))
        beta = np.sqrt(1-Mcruise)  # correct for compressibility
        return Cfi/beta
    
    Cf = SkinFrict(Aircraft.ParAnFP.M_cruise, ComputeRe())
    shape_factor = 3.0
    d_wh = 3.
    tc_limit = Compute_tc_limit(Aircraft, CL, sweep)
    return 2 * d_wh * (1 + shape_factor * tc_limit) * Cf


def Computetau(Aircraft, ISA_model):
    # Compute rel. pressure
    T, p, rho = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])
    delta     = p/ISA_model.p0
    
    # Get Take-off thrust and cruise thrust
    T_to = Aircraft.ParAnFP.T_to
    T_cruise = Aircraft.ParAnFP.Thrust
    
    tau = T_cruise/delta/T_to #thrust lapse rate
    
    return tau

def ComputeFprop(Aircraft, ISA_model, TSFC):
    
    # Compute rel. pressure
    T, p, rho = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])
    delta     = p/ISA_model.p0
    
    # Get constants
    muT = ComputemuT(Aircraft) # Wpp/T_TO
    tau = Computetau(Aircraft, ISA_model)
    Hg  = 4350 #km
    eta_0 = OverallEff(Aircraft, ISA_model, TSFC)
    Req = Aircraft.ParAnFP.s_cruise/1e3
    
    
    return Req/eta_0/Hg + muT / tau / delta

def ComputeFWP(Aircraft, Fprop, theta2, theta3, Aw, CL, sweep):
    
    # Constants
    CDc = 0.0010
    eCurl = 0.80
    # Compute wing profile drag
    CDpCurl = ComputeCDpCurl(Aircraft, CL, sweep)
    
    # Compute t/c upper limit
    tc_limit = Compute_tc_limit(Aircraft, CL, sweep)
    
    FWP1 = theta3 * Aw * np.sqrt(Aw / CL) / tc_limit
    FWP2 = theta2 / CL
    
    FWP3 = (CDpCurl + CDc) / CL + CL / (np.pi*Aw*eCurl)
    
    FWP  = FWP1 + FWP2 + FWP3
    
    return FWP

def ComputePartialSweepOpt(Aircraft):
    
    return np.arccos(0.75*0.935/Aircraft.ParAnFP.Mdd)


def ComputePartialCLopt(Aircraft, ISA_model, theta2, theta3, 
                        Fprop, TSFC, Aw, sweep, CL):
    
    from scipy.optimize import minimize_scalar
    
    def CL_trans(CLi):
        
        # Compute profile drag (wing)
        CDpCurl  = ComputeCDpCurl(Aircraft, CLi, sweep)
        tc_limit = Compute_tc_limit(Aircraft, CLi, sweep)
        
        
        CDFactor = np.sqrt(CDpCurl * np.pi * Aw * eCurl)
        term2    = (0.5 * theta3 * Aw * np.sqrt(Aw * CLi) /
                    (CDpCurl * Fprop * tc_limit))
        term3    = theta2 / (CDpCurl * Fprop)
#        print(CDFactor, term2, term3, tc_limit)
        return (CLi - CDFactor * (1 + term2 + term3)**0.5)
    
    # Constants
    eCurl    = 0.80
    Fprop    = ComputeFprop(Aircraft, ISA_model, TSFC)
#    
    # Find all optimum CL for given sweep
#    CL_opt = fmin(lambda x: -CL_trans(x), 0.1, disp = False)
    CL_opt = minimize_scalar(lambda x: -CL_trans(x), bounds = (CL[0], CL[-1]), 
                             method = 'bounded')
    return CL_opt

def ComputePartialAwOpt(Aircraft, ISA_model,
                        theta2, theta3, Fprop, TSFC, sweep, CL):
    
    # Constants
    eCurl = 0.80
    Fprop = ComputeFprop(Aircraft, ISA_model, TSFC)
    Mcrit = 0.935
    Mdd   = Aircraft.ParAnFP.Mdd
    
    Aw_opt = (CL**0.6 * (2 * Fprop / (3 * np.pi * eCurl * theta3) * 
                        (np.cos(sweep)**3 * (Mcrit - Mdd * np.cos(sweep))
                         - 0.11 * CL**1.5))**0.4)
    
    return Aw_opt


def ComputeSpanLoading(Aircraft, ISA_model, Fprop, theta2, theta3, TSFC,
                       sweep, CL):
    
    # Constants
    Fprop = ComputeFprop(Aircraft, ISA_model, TSFC)
    tc_limit = Compute_tc_limit(Aircraft, CL, sweep)
    
    # Compute profile drag
    CDpCurl = ComputeCDpCurl(Aircraft, CL, sweep)
    
    return CL**(-1/3) * ((CDpCurl * Fprop + theta2)/theta3 * tc_limit)**(2/3)

def ComputeSpanLoadingCL(Aircraft, ISA_model, Fprop, theta2, theta3, TSFC,
                       sweep, Aw, CL):
    
    # Constants
    Fprop = ComputeFprop(Aircraft, ISA_model, TSFC)
    tc_limit = Compute_tc_limit(Aircraft, CL, sweep)
    
    # Compute profile drag
    CDpCurl = ComputeCDpCurl(Aircraft, CL, sweep)
    
    return (((CDpCurl * Fprop + theta2)/theta3 * tc_limit)**(2/3)/Aw)**3
    