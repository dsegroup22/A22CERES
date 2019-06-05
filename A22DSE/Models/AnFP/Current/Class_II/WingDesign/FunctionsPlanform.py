# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:47:32 2019

@author: hksam
"""
#sys.path.append('../')
import os
from pathlib import Path
os.chdir(Path(__file__).parents[6])
from A22DSE.Models.AnFP.Current.InitialSizing import AnFP_Exec_CD0


# =============================================================================
# UNFINISHED WORK
# =============================================================================
import numpy as np
from scipy.optimize import fsolve
    
#def OptimalARWing(CL, Fprop, phi_3):
#    ''' INPUT: Eq. lift-coefficient [-], Propulsion weight penalty, phi_3,
#    semi-analytical relationship, drag-divergence Mach number [-]
#    , critica Mach number, Sweep angle [rad]
#    OUTPUT: Aspect Ratio of the wing
#    DESCRIPTION: Computes the partial optimal AR of the wing using the method
#    described in Torenbeek CH10. In this method, the AR is optimised in minimum
#    MTOW (due to wing penalty).'''
#    eCurl = np.average([0.9,0.95])
#    Aw = np.power(CL,0.6)*(2*Fprop/(3*np.pi*eCurl))
#    
#    return Aw

def friction_coef(Aircraft):
    '''
    INPUT: V_cruise, atmospheric conditions, span, wetted area
    OUTPUT: friction coefficient
    DESCRIPTION: Copied from Nikki's CD0 program
    '''
    anfp = Aircraft.ParAnFP
    V = anfp.V_cruise #Cruise speed
    b = anfp.b #Span
    
    mu = 1.43226e-5 #dynamic friction
    rho = 0.0880349 #density
    nu = mu / rho #kinematic friction
    
    S_wet = S_wet_wing(Aircraft) + S_wet_fuselage(Aircraft) + \
    S_wet_tail(Aircraft) + S_wet_engine(Aircraft)
    
    Re = (S_wet / b) * V / nu
    C_fe = 0.00258 + 0.00102*np.exp(-6.28e-9 * Re) + 0.00295*np.exp(-2.01e-8*\
                                   Re)
    return C_fe, S_wet

def DynamicPressEq(Aircraft, ISA_model):
    
    # CONSTANTS AND VARIABLES
    AnFP = Aircraft.ParAnFP
    ISAFunc = ISA_model.ISAFunc
    h_cruise = AnFP.h_cruise
#    h_cruise = 11000
    
    # Compute Mach number
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise]))[0]
    Mcruise = AnFP.V_cruise/a
    P = ISAFunc([h_cruise])[1]
    
    # Compute dynamic pressure eq.
    q_eq = 0.5*ISA_model.gamma*np.power(Mcruise, 2)*1.025*P
    
    return q_eq

def ComputeCL_eq(ISA_model, MTOWi, Aircraft):
    ''' INPUT:
    OUTPUT: returns CL_hat
    DESCRIPTION: Returns CL_hat based on (independent) wing loading and the
    Mach number it flies at and wing surface area. This is a selection
    variable.'''
        
    #DEFINE VARIABLES
    AnFP = Aircraft.ParAnFP
    ISAFunc = ISA_model.ISAFunc
    h_cruise = Aircraft.ParAnFP.h_cruise
#    MTOW = Aircraft.ParStruc.MTOW
    
    # Compute Mach number
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise])[0])
    Mcruise = AnFP.V_cruise/a
    P = ISAFunc([h_cruise])[1]
    
#    print ("Mcruise: " + repr(Mcruise) + " P: " + repr(P) + " h: " + 
#           repr(h_cruise))
    #Compute CL_hat
    # TODO: Verify S == Sw and M is indeed the cruise Mach.
    CL_hat = MTOWi*ISA_model.g0/ \
    (0.5*ISA_model.gamma*np.power(Mcruise,2)*1.025*AnFP.S
                    *P)
    
#    print(CL_hat)
    return CL_hat
def ComputeTheta1(Aircraft, ISA_model):
    '''
    INPUT: returns dimless. quasi-analytical parameter for transonic planform
    sizing
    OUTPUT: returns theta_1
    DESCRIPTION: returns theta_1 required for the optimisation and class II
    sizing of subsonic wing planform design
    '''
    #CONSTANTS
        ##TODO: Get actual fuel mass from NOUT and RICK
    Mfuel = 10000
    MZFW  = Aircraft.ParStruc.MTOW - Mfuel
    rh = 0.10                               # ratio Wing weight / wing horiz.
    q_des = DynamicPressEq(Aircraft, ISA_model)
    bref = 100 #m
    nult = 2.5
    tc   = Aircraft.ParAnFP.tc
    taper = Aircraft.ParAnFP.taper
    nep  = 0.36 * (1 + taper)**0.5
    sweep = np.deg2rad(5)
    
    theta1 = 0.0013*(1+rh)*np.sqrt(MZFW*ISA_model.g0/q_des)/bref *nult*nep /\
    (tc*np.cos(sweep)**2)
    
    return theta1
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
    q_des = DynamicPressEq(Aircraft, ISA_model)
    omegaS = 210  # N/m for ALUMINIUM WING
    
    return (1+rh)*omegaS/q_des

def ComputeTheta3(Aircraft, ISA_model):
    '''INPUT:
       OUTPUT: returns dimless. quasi-analytical parameter for transonic
       planform sizing
       DESCRIPTION: Returns theta_3, which replaces theta_1 in the design of 
       transonic planform design. As a result, two additional selection
       variables can be used. Namely, (t/c) and the sweep angle of the wing.
    '''
    
    
    #TODO: Taper ratio wing inside Aircraft object or individual constant?
    #TODO: Find proper bref value
    #TODO: rh is approx. 0.10; CHANGE when Class II weights are set up.
    #TODO: fuelused is gone, set to 5000 kg
    
    # CONSTANTS AND VARIABLES
    rh = 0.10               # typical value
    fuelused = 10000         #kg
    MZFW = (Aircraft.ParStruc.MTOW - fuelused)*ISA_model.g0  #MZFW = MTOW-Mfuel
    bref = 100           
    mu_cp = 0.36*np.power((1+Aircraft.ParAnFP.taper), 0.5)
    n_ult = 2.5
    q_eq = DynamicPressEq(Aircraft, ISA_model)
    
    
    return 0.0013*(1+rh)*mu_cp*n_ult*np.sqrt(MZFW/q_eq)/bref

def CDpCurlFunc(Aircraft, ISA_model, Sweepi):
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''    
    def SkinFrict(Mcruise, Re):
        Cfi = 0.455/(np.power(np.log10(Re),2.58))
        beta = np.sqrt(1-Mcruise)
        return Cfi/beta
    
    def CDpCurlWing(Cf):
        r_theta = np.average([2.5,3.5])

        return 2*(1+r_theta*AnFP.tc*np.power(np.cos(Sweepi),2))*Cf
    
    def Dw_and_h():
    # TODO: Find out how to find CDp_h
        return (1.2+1.3)/2
    
    def ComputeRe():

        if np.abs((h_cruise-20000)/20000) <= 0.05:
            v = 0.0000143226
        else:
            ValueError("Not programmed yet\n")
        u = AnFP.V_cruise
        L = AnFP.MAC
        return u*L/v

    
    #DEFINE VARIABLES
    AnFP = Aircraft.ParAnFP
    ISAFunc = ISA_model.ISAFunc
    h_cruise = Aircraft.ParAnFP.h_cruise
    Re = ComputeRe()/2.4
    
    #COMPUTE Mach number
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise]))[0]
    Mcruise = AnFP.V_cruise/a
    
    #COMPUTE mult. factor due to horizontal tail
    Cfw = SkinFrict(Mcruise, Re)
    
    #COMPUTE final CDpCurl
    CDpCurl = 2 * Dw_and_h() * CDpCurlWing(Cfw)
    
    return CDpCurl

def ComputeFprop(Aircraft, ISA_model, MTOWi):
    from scipy.optimize import fsolve
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''    
    def ComputeDragNacelle(Cdi, D):
        return (0.5*ISA_model.ISAFunc([h_cruise])[2]*
                AnFP.V_cruise**2*np.pi*D**2/4*Cdi)
    
    def ComputeTaubar():
        AtmosDelta =  0.0540
#        return (T-Dnac)/(AtmosDelta*T_TO)
        return 0.55
    def deltaTrans(delta):
#        global mu_T, tau_bar, eta_0bar, Hg, Req, deltaMD
        return delta-deltaMD*np.sqrt(1+2*mu_T/(tau_bar*delta)*eta_0bar*Hg/Req)
    
    AnFP = Aircraft.ParAnFP
#    Struct = Aircraft.ParStruc
    ISAFunc = ISA_model.ISAFunc
    h_cruise = Aircraft.ParAnFP.h_cruise
    ConversTool = Aircraft.ConversTool
    lbf2N       = 4.44822
    WfuMTOW = 0.20
    C_T = 0.56*ConversTool.lbs2kg/lbf2N
    Rmis  = Aircraft.ParAnFP.s_cruise       # mission range
    Rlost = False                           # range lost dependent on CdM
                                            # zero below Mcrit
    Hg = 4350*1000.                         # for conv. gas turbine engine fuel
    theta = 0.7519                          # rel. density
    
    

    q0 = ISA_model.rho0*0.5*AnFP.V_cruise**2
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise]))[0]
    Mcruise = AnFP.V_cruise/a
    Cdi = 0.04                                      #Cranfield report
    #TODO: Add engine diameter in class structure
    Diameter = 1.61                     #[m]
    mu_T = 0.26
    T = 113120.                                     #values for IAE V2531
    T_TO = 139360.                                  #values for IAE V2531
    Cldes = 0.56                                    #airfoil

    #compute mu_0
    eta_0 = 0.0287*Mcruise/(C_T/np.sqrt(theta))
    Dnac = ComputeDragNacelle(Cdi, Diameter)
    eta_0bar = eta_0*(1-Dnac/T)
    Req = (Rmis+Rlost)*(1-0.5*WfuMTOW)
    tau_bar = ComputeTaubar()
    
    # compute delta
    deltaMD = MTOWi/(q0*Cldes*AnFP.S)*ISA_model.g0
    delta = fsolve(deltaTrans, 0.9)
#    print (Dnac)
    Fprop = Req/(eta_0bar*Hg) + mu_T/(tau_bar*delta)
#    print (Req/(eta_0bar*Hg), mu_T/(tau_bar*delta))
    return Fprop

def ComputeAw(Aircraft, ISA_model, MTOWi, Sweepi):
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''
    Fprop = ComputeFprop(Aircraft, ISA_model, MTOWi)
    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    theta2 = ComputeTheta2(Aircraft, ISA_model)
    theta3 = ComputeTheta3(Aircraft, ISA_model)
    CL_eq = ComputeCL_eq(ISA_model, MTOWi, Aircraft)
    return np.power((CDpCurl*Fprop+theta2)/theta3, 2/3)/np.power(CL_eq, 1/3)

def FWP_subsonic(Theta1, Theta2, Aircraft, ISA_model, Awi, MTOWi, CL):
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''    
    #prerequisites:
    sweep = np.deg2rad(5)
    Fprop = ComputeFprop(Aircraft, ISA_model, MTOWi)
    CDpcurl = CDpCurlFunc(Aircraft, ISA_model, sweep)
    e       = Aircraft.ParAnFP.e
    
    FWP1 = Theta1*Awi*np.sqrt(Awi/CL)
    FWP2 = Theta2/CL
    FWP3 = Fprop * (CDpcurl / CL + CL / (np.pi*Awi*e))
    
    FWP = FWP1 + FWP2 + FWP3
    
    return FWP

#def ComputeMTOW(Aircraft, ISA_model, MTOWi, Aw, CL, FWP):
#    from scipy.optimize import fsolve
#    #TODO 90% is assumed, see eq. 10.15
#    
#    W_num = 10000
#    W_denum = 0.76
#    sweep = np.deg2rad(5)
#    Fprop = ComputeFprop(Aircraft, ISA_model, MTOWi)
#    CDp   = CDpCurlFunc(Aircraft, ISA_model, sweep)
#    CDpS  = CDp*Aircraft.ParAnFP.S
#    FWP   = FWP_subsonic(Theta)
#    
#    MTOW - (W_num + DynamicPressEq(Aircraft, ISA_model)*Fprop*CDpS)
#    
#    return
    
def ComputeCDpS(Aircraft):
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''
    S_wet=AnFP_Exec_CD0.friction_coef(Aircraft)[1]
    C_f=AnFP_Exec_CD0.friction_coef(Aircraft)[0]
    
    return 0.7*S_wet*C_f

def ComputeCurveII(Aircraft, ISA_model, C_l):
    MTOW=500000
    Fprop=ComputeFprop(Aircraft, ISA_model, MTOW)
    theta1=ComputeTheta1(Aircraft, ISA_model)
    eCurl = np.average([0.9,0.95])
    CII=C_l**0.6*(2/3*Fprop/theta1/eCurl)**0.4
    
    return CII

def GetOptCLCurve(Aircraft, ISA_model, MTOWi, Sweepi, Awi):
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''
    
    #constants
    eCurl = np.average([0.9,0.95])
    
    #prerequisites
    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    Theta1  = ComputeTheta1(Aircraft, ISA_model)
    Theta2  = ComputeTheta2(Aircraft, ISA_model)
    Fprop   = ComputeFprop(Aircraft, ISA_model, MTOWi)
    
    def TransCL(CL):
        
        y = CL - np.sqrt(CDpCurl * np.pi * Awi * eCurl) * \
        (1 + (0.5 * Theta1 * Awi * np.sqrt(Awi * CL) + Theta2)/(CDpCurl*Fprop)\
         )**(0.5)
        
        return y
    
    CL_des = fsolve(TransCL, 0.50)
    
    return CL_des

def GetTankVolume(Aircraft, ISA_model, Awi):
    '''
    INPUT: 
    OUTPUT:
    DESCRIPTION:
    '''
    #constants
    mu_tank = 0.55
    tc = Aircraft.ParAnFP.tc
    Sw = Aircraft.ParAnFP.S

    
    
    return 0.90*mu_tank*tc*Sw**1.5*Awi**(-.5)
    
def GetWfCurve(Aircraft, ISA_model, Awi, MTOWi, CLi, Sweepi):

    return None

def ComputeCurveC2(Aircraft, ISA_model,C_l):
    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, 5/180*np.pi)
    print (CDpCurl)
    theta_1 = ComputeTheta1(Aircraft, ISA_model)
    print (theta_1)
    theta_2 = ComputeTheta2(Aircraft, ISA_model)
    print (theta_2)
    eCurl = np.average([0.9,0.95])
    print (eCurl)
    from scipy.optimize import fsolve
    def  f(A_w):
        f=(1.5*CDpCurl*np.pi*eCurl*A_w)**0.5*(1-theta_2/(theta_1*(A_w**1.5)*C_l**0.5))**(-0.5) - C_l
        return f
    C2=fsolve(f,6)
    return C2


    #Abbreviations
    ConversTool = Aircraft.ConversTool
    AnFP = Aircraft.ParAnFP
    ISAFunc = ISA_model.ISAFunc
    
    ##Constants
    WresfMTOW = 0.045
#    WfuMTOW   = 0.20
    Hg      = 4350*1000.                    # for conv. gas turbine engine fuel    
    theta = 0.7519                          # rel. density   
    C_T = 0.56*ConversTool.lbs2kg/ConversTool.lbf2N
    h_cruise = AnFP.h_cruise
    eCurl    = np.average([0.90, 0.95])
    #prerequisites
    Rm      = Aircraft.ParAnFP.s_cruise ##maximum range
#    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    q = ISAFunc([h_cruise])[-1]*0.5*AnFP.V_cruise**2
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise]))[0]
    Mcruise = AnFP.V_cruise/a
    eta_0 = 0.0287*Mcruise/(C_T/np.sqrt(theta))    
    CDp    = ComputeCDpS(Aircraft)/AnFP_Exec_CD0.friction_coef(Aircraft)[1]
    
    #Determine CDS
    CD = 1/Aircraft.ParAnFP.LD*CLi
    CDS = CD*AnFP_Exec_CD0.friction_coef(Aircraft)[1]
    
    Wfmax  = Rm/(eta_0*Hg)*(CDp/CLi+CLi/(np.pi*Awi*eCurl)*MTOWi + \
             q*CDS) + WresfMTOW* MTOWi
    
    return Wfmax

#MTOWi=Conv.ParStruc.MTOW
#Sweepi=np.deg2rad(5)
#y1=np.linspace(4,12,20)
#x1=GetOptCLCurve(Conv, ISA_model, MTOWi, Sweepi, y1)
#
x2=np.linspace(0.3,1,3,20)
y2= ComputeCurveII(Conv, ISA_model, x2)

import matplotlib.pyplot as plt
plt.plot(x2,y2)