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
#           FUNCTIONS FOR SUBSONIC WING PLANFORM DESIGN
# =============================================================================
import numpy as np
from scipy.optimize import fsolve

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
    '''
    INPUT: Aircraft and ISA model
    OUTPUT: equivalent dynamic pressure coeff.
    DESCRIPTION: Computes the dynamic pressure coeff and corrects it for the
    fuel lost during climb and take-off by decreasing the MTOW by 2.5%
    '''
    # CONSTANTS AND VARIABLES
    AnFP = Aircraft.ParAnFP
    ISAFunc = ISA_model.ISAFunc
    h_cruise = AnFP.h_cruise
    
    # Compute Mach number
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise]))[0]
    Mcruise = AnFP.V_cruise/a
    P = ISAFunc([h_cruise])[1]
    
    
    # Compute dynamic pressure eq.
    q_eq = 0.5*ISA_model.gamma*np.power(Mcruise, 2)*1.025*P
    
    return q_eq

#def ComputeCL_eq(ISA_model, MTOWi, Aircraft):
#    ''' INPUT:
#    OUTPUT: returns CL_hat
#    DESCRIPTION: Returns CL_hat based on (independent) wing loading and the
#    Mach number it flies at and wing surface area. This is a selection
#    variable.'''
#        
#    #DEFINE VARIABLES
#    AnFP = Aircraft.ParAnFP
#    ISAFunc = ISA_model.ISAFunc
#    h_cruise = Aircraft.ParAnFP.h_cruise
#    
#    # Compute Mach number
#    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise])[0])
#    Mcruise = AnFP.V_cruise/a
#    P = ISAFunc([h_cruise])[1]
#    
#    CL_hat = MTOWi*ISA_model.g0/ \
#    (0.5*ISA_model.gamma*np.power(Mcruise,2)*1.025*AnFP.S
#                    *P)
#    
##    print(CL_hat)
#    return CL_hat
    
def ComputeTheta1(Aircraft, ISA_model, Sweepi):
    '''
    INPUT: returns dimless. quasi-analytical parameter for transonic planform
    sizing
    OUTPUT: returns theta_1
    DESCRIPTION: returns theta_1 required for the optimisation and class II
    sizing of subsonic wing planform design
    '''
    #CONSTANTS
        ##TODO: Get actual fuel mass from NOUT and RICK
        #TODO: Change taper and MZFW, Mfuel
    WfuMTOW = Aircraft.ParStruc.wfratioclimb
    Mfuel = WfuMTOW*Aircraft.ParStruc.MTOW
    MZFW  = Aircraft.ParStruc.MTOW - Mfuel
    rh = 0.10                               # ratio Wing weight / wing horiz.
    q_des = DynamicPressEq(Aircraft, ISA_model)
    bref = 100 #m
    tc   = Aircraft.ParAnFP.tc
    taper = Aircraft.ParAnFP.taper
    nep  = 0.36 * (1 + taper)**0.5
    n_ult = Aircraft.ParAnFP.n_ult
    
    theta1 = 0.0013*(1+rh)*np.sqrt(MZFW*ISA_model.g0/q_des)/bref *n_ult*nep /\
    (tc*np.cos(Sweepi)**2)
    
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
    omegaS = 250  # N/m² for ALUMINIUM WING
    
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
    
    # CONSTANTS AND VARIABLES
    rh = 0.10               # typical value
    WfuMTOW = Aircraft.ParStruc.wfratio
    fuelused = WfuMTOW*Aircraft.ParStruc.MTOW
    MZFW = (Aircraft.ParStruc.MTOW - fuelused)*ISA_model.g0  #MZFW = MTOW-Mfuel
    bref = 100           
    mu_cp = 0.36*np.power((1+Aircraft.ParAnFP.taper), 0.5)   # pg.236 Torenbeek
    n_ult = Aircraft.ParAnFP.n_ult
    q_eq = DynamicPressEq(Aircraft, ISA_model)
    
    
    return 0.0013*(1+rh)*mu_cp*n_ult*np.sqrt(MZFW/q_eq)/bref

def CDpCurlFunc(Aircraft, ISA_model, Sweepi):
    '''
    INPUT: Aircraft, ISA calculator, sweep of the wing (single-valued)
    OUTPUT: corrected profile drag for the wing and horizontal tail
    DESCRIPTION: Area variation and Reynold's number affect the profile drag,
    therefore the drag area is proportional to the wing surface area and is
    proportional to Sw**.92.
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
        '''
        Computes the experienced Re of the chord
        '''
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
    Re = ComputeRe()
#    print(Re)
    
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
    INPUT : Aircraft, ISA calculator, MTOW (single-valued)
    OUTPUT: Propulsion Penalty Function, Fprop
    DESCRIPTION:
    The propulsion function is a function of altitude and wing loading. The
    equation assume
    - tau_bar is 0.55 as mentioned by Torenbeek as a "typical
    value". 
    - A/C uses typical jet fuel
    - flies at h = 20km for rel. density
    - mu_T is assumed as a "typical value"
    - Induced drag coeff. of the engine nacelle is acquired from Cranfield
        for typical transonic-operating engines
    '''
    def ComputeDragNacelle(Cdi, D):
        return (0.5*ISA_model.ISAFunc([h_cruise])[2]*
                AnFP.V_cruise**2*np.pi*D**2/4*Cdi)
    
    def ComputeTaubar():
#        AtmosDelta =  0.0540
#        return (T-Dnac)/(AtmosDelta*T_TO)
        return 0.55
    def deltaTrans(delta):
#        global mu_T, tau_bar, eta_0bar, Hg, Req, deltaMD
        return delta-deltaMD*np.sqrt(1+2*mu_T/(tau_bar*delta)*eta_0bar*Hg/Req)
    
    AnFP = Aircraft.ParAnFP
#   Struct = Aircraft.ParStruc
    ISAFunc = ISA_model.ISAFunc
    h_cruise = Aircraft.ParAnFP.h_cruise
    ConversTool = Aircraft.ConversTool
    lbf2N       = 4.44822
    WfuMTOW = Aircraft.ParStruc.wfratio
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
    
    TcontTTO = 0.9
    T = 60000.*TcontTTO                              #values for EJ200
    T_TO = 60000.                                  #values for EJ200
    Cldes = 0.56                                    #airfoil

    #compute eta_0
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
#    return 3

#def ComputeAw(Aircraft, ISA_model, MTOWi, Sweepi):
#    '''
#    INPUT: 
#    OUTPUT:
#    DESCRIPTION:
#    '''
#    Fprop = ComputeFprop(Aircraft, ISA_model, MTOWi)
#    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, Sweepi)
#    theta2 = ComputeTheta2(Aircraft, ISA_model)
#    theta3 = ComputeTheta3(Aircraft, ISA_model)
#    CL_eq = ComputeCL_eq(ISA_model, MTOWi, Aircraft)
#    return np.power((CDpCurl*Fprop+theta2)/theta3, 2/3)/np.power(CL_eq, 1/3)

def FWP_subsonic(Theta1, Theta2, Aircraft, ISA_model, Awi, MTOWi, CL):
    '''
    INPUT: Theta1, Theta2, Aircraft, ISA calculator, single-valued AR,
    single-valued MTOW, single-valued CL
    OUTPUT: wing penalty function
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
    INPUT: Aircraft model
    OUTPUT: Profile drag area CDpS [m²]
    DESCRIPTION: Determines the profile drag area of the aircraft by computing
    the wetted area and the friction coefficient.
    '''
    S_wet=AnFP_Exec_CD0.friction_coef(Aircraft)[1]
    C_f=AnFP_Exec_CD0.friction_coef(Aircraft)[0]
    
    return 0.7*S_wet*C_f

def ComputeCurveII(Aircraft, ISA_model, C_l, MTOWi, Sweepi):
    ''' 
    INPUT: Aircraft Model, ISA model, single-valued lift coeff., MTOW, and
    sweep
    OUTPUT: optimum aspect ratio given the MTOW (which does not necessarily
    mean optimum CL as well)
    DESCRIPTION: Constraint II in the graph as shown by Torenbeek in fig. 10.6
    The constraint is the partial deriv. of the FWP w.r.t. Aw, (aspect ratio
    of the wing), where FWP = f(A, CL(, t/c, sweep)). The analytical
    equation is shown in Equation (10.27).
    '''

    Fprop=ComputeFprop(Aircraft, ISA_model, MTOWi)
    theta1=ComputeTheta1(Aircraft, ISA_model, Sweepi)
    
    #Oswald factor for plane wing, different than the Oswald factor for drag
    #polar
    eCurl = np.average([0.9,0.95])                  
    CII=C_l**0.6*(2/3*Fprop/theta1/eCurl/np.pi)**0.4
    
    return CII

def GetOptCLCurve(Aircraft, ISA_model, MTOWi, Sweepi, Awi):
    '''
    INPUT: Aircraft model, ISA model, single-valued MTOW, single-valued sweep,
    single-valued A
    OUTPUT: Optimum design lift design coeff for given MTOW.
    DESCRIPTION: Implementation of Equation 10.17 as described in Torenbeek
    Chapter 10, Advanced Aircraft Design. 
    Constraint I in the graph as shown by Torenbeek in fig. 10.6
    The constraint is the partial deriv. of the FWP w.r.t. Aw, (aspect ratio
    of the wing), where FWP = f(A, CL(, t/c, sweep)).
    '''
    
    #constants
    eCurl = np.average([0.9,0.95])
    
    #prerequisites
    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    Theta1  = ComputeTheta1(Aircraft, ISA_model, Sweepi)
#    Theta1  = ComputeTheta3(Aircraft, ISA_model)
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
    INPUT: Aircraft model, ISA model, and single-valued aspect ratio
    OUTPUT: Fuel tank volume in m³
    DESCRIPTION: Estimation of the fuel tank volume in the wing assuming that
    all the fuel is stored inside the wing. It is a function of the aspect
    ratio and the equation is given by Equation (10.30).
    '''
    #constants
    mu_tank = 0.55
    tc = Aircraft.ParAnFP.tc
    Sw = Aircraft.ParAnFP.S

    
    
    return 0.90*mu_tank*tc*Sw**1.5*Awi**(-.5)
    
def GetWfCurve(Aircraft, ISA_model, Awi, MTOWi, CLi, Sweepi):
    '''
    INPUT: Aircraft model, ISA model, single-valued: A, MTOW, CL, Sweep
    OUTPUT: Maximum fuel weight [N]
    DESCRIPTION: 
    See Equation (10.31).
    '''

    ##TODO: Change WfuMTOW = Aircraft.ParStruc.wfratio    
    ## ASSUMPTION: Rm = Rcruise
    ##             CDS = LD
    
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

def ComputeCurveC2(Aircraft, ISA_model,C_l):
    ''' 
    INPUT: Aircraft model, ISA model, and single-valued lift coefficient
    OUTPUT: Aspect ratio given wing and tail weight fraction
    DESCRIPTION: Optimum AR given a upper limit by the wing and tail weight
    for minimum MTOW and fuel weight.
    '''
    
    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, np.deg2rad(5))
#    print (CDpCurl)
    theta_1 = ComputeTheta1(Aircraft, ISA_model, Sweepi)
#    print (theta_1)
    theta_2 = ComputeTheta2(Aircraft, ISA_model)
#    print (theta_2)
    eCurl = np.average([0.9,0.95])
#    print (eCurl)
    from scipy.optimize import fsolve
    def  f(A_w):
        b = (1-theta_2 /(theta_1*(A_w**1.5)*C_l**0.5))**(-0.5)
#        print (A_w, b, theta_2 /(theta_1*(A_w**1.5)*C_l**0.5) )
        f = C_l - (1.5*CDpCurl*np.pi*eCurl*A_w)**0.5*(1-theta_2 /\
          (theta_1*(A_w**1.5)*C_l**0.5))**(-0.5)
        return f
    C2= fsolve(f,15)
    return C2

def ComputeAw(Aircraft, ISA_model, Sweepi):
    ''' 
    INPUT: Aircraft model, ISA model, single-valued sweep
    OUTPUT: Optimum AR for optimum CL AND FWP
    DESCRIPTION:
        Finds the intersection of the UNCONSTRAINED optima of the FWP function.
        For given MTOW the function finds the associated optimal aspect ratio
        for optimal lift coefficient.
        
    '''
    MTOWi= Aircraft.ParStruc.MTOW*9.81
    CdpCurl=CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    Fprop=ComputeFprop(Aircraft, ISA_model, MTOWi)
    Theta1=ComputeTheta1(Aircraft, ISA_model, Sweepi)
    Theta2=ComputeTheta2(Aircraft, ISA_model)
    eCurl = np.average([0.9,0.95])
    Aw=(CdpCurl+Theta2/Fprop)**(3/7)*(1.5*np.pi*eCurl)**(-1/7)*\
    (Fprop/Theta1)**(4/7)
    return Aw


def ComputeCl(Aircraft,ISA_model, Sweepi):
    ''' 
    INPUT: Aircraft model, ISA model, single-valued sweep
    OUTPUT: Optimum CL for optimum AR AND FWP
    DESCRIPTION:
        Finds the intersection of the UNCONSTRAINED optima of the FWP function.
        For given MTOW the function finds the associated optimal CL
        for optimal AR.
    '''
    MTOWi=Aircraft.ParStruc.MTOW*9.81
    CdpCurl=CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    Fprop=ComputeFprop(Aircraft, ISA_model, MTOWi)
    Theta1=ComputeTheta1(Aircraft, ISA_model, Sweepi)
    Theta2=ComputeTheta2(Aircraft, ISA_model)
    eCurl = np.average([0.9,0.95])
    Cl=(CdpCurl+Theta2/Fprop)**(5/7)*(1.5*np.pi*eCurl)**(3/7)*\
    (Fprop/Theta1)**(2/7)
    return Cl


def GetTransOptAw(Aircraft, ISA_model, CL_eq, MTOWi, sweep):
    ''' 
    INPUT: Aircraft model, ISA model, single-valued: CL, MTOW and sweep
    OUTPUT: the optimum Aw for given CL, sweep and MTOW
    DESCRIPTION: Optimum transonic wing aspect ratio for given MTOW, similarly
    to definition for curve II. The analytical equation is shown in Equation
    (10.52).
    '''    
    Mcrit = 0.935
    Mdd = Aircraft.ParAnFP.Mdd
    Fprop = ComputeFprop(Aircraft, ISA_model, MTOWi)
    theta3 = ComputeTheta3(Aircraft, ISA_model)
    eCurl = np.average([0.9, 0.95]) 
    
    return (CL_eq**0.6*(2*Fprop/(3*np.pi*theta3*eCurl)*(np.cos(sweep)**3*(
            Mcrit-Mdd*np.cos(sweep))-0.11*CL_eq**1.5))**0.4)
