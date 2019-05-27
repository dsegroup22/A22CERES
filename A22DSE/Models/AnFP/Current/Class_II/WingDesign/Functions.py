# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:47:32 2019

@author: hksam
"""


# =============================================================================
# UNFINISHED WORK
# =============================================================================
import numpy as np

class airfoil(object):
    
    def __init__(self, tc, LD, Cldes, Cd0, Clmax, Cm0):
        
        self.tc = tc
        self.LD = LD
        self.Cldes = Cldes
        self.Cd0 = Cd0
        self.Clmax = Clmax
        self.Cm0 = Cm0
    
    def ComputeMdd(self):
        Mcrit = 0.935                   #2nd gen supercrit. airfoil, see TBeek
        return Mcrit - self.tc - 0.10*np.power(self.cl,1.5)
        
        

def OptimalARWing(CL, Fprop, phi_3):
    ''' INPUT: Eq. lift-coefficient [-], Propulsion weight penalty, phi_3,
    semi-analytical relationship, drag-divergence Mach number [-]
    , critica Mach number, Sweep angle [rad]
    OUTPUT: Aspect Ratio of the wing
    DESCRIPTION: Computes the partial optimal AR of the wing using the method
    described in Torenbeek CH10. In this method, the AR is optimised in minimum
    MTOW (due to wing penalty).'''
    eCurl = np.average([0.9,0.95])
    Aw = np.power(CL,0.6)*(2*Fprop/(3*np.pi*eCurl))
    
    return Aw

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
    q_eq = DynamicPressEq(Aircraft, ISA_model)
    omegaS = 210  # N/m for ALUMINIUM WING
    
    return (1+rh)*omegaS/q_eq

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
    
    # CONSTANTS AND VARIABLES
    rh = 0.10               # typical value
    MZFW = Aircraft.ParStruc.MTOW - Aircraft.ParAnFP.fuelused#MZFW = MTOW-Mfuel
    bref = Aircraft.ParAnFP.b            
    mu_cp = 0.36*np.power((1+Aircraft.ParAnFP.TRw), 0.5)
    n_ult = 2.5
    q_eq = DynamicPressEq(Aircraft, ISA_model)
    
    return 0.0013*(1+rh)*mu_cp*n_ult*np.sqrt(MZFW/q_eq)/bref

def CDpCurlFunc(Aircraft, ISA_model, Sweepi):
    
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
    Re = ComputeRe()
    
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
    Rmis  = Aircraft.ParAnFP.s_cruise       # mission range
    Rlost = False                           # range lost dependent on CdM
                                            # zero below Mcrit
    Hg = 4350*1000.                         # for conv. gas turbine engine fuel
    q0 = ISA_model.rho0*0.5*AnFP.V_cruise**2
    theta = 0.7519                          # rel. density
    a = np.sqrt(ISA_model.gamma*ISA_model.R*ISAFunc([h_cruise]))[0]
    Mcruise = AnFP.V_cruise/a
    
    C_T = 0.56*ConversTool.lbs2kg/lbf2N
    Cdi = 0.04                                      #Cranfield report
    #TODO: Add diameter in class structure
    Diameter = 1.61                     #[m]
    WfuMTOW = AnFP.fuelused/MTOWi
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
    Fprop = ComputeFprop(Aircraft, ISA_model, MTOWi)
    CDpCurl = CDpCurlFunc(Aircraft, ISA_model, Sweepi)
    theta2 = ComputeTheta2(Aircraft, ISA_model)
    theta3 = ComputeTheta3(Aircraft, ISA_model)
    CL_eq = ComputeCL_eq(ISA_model, MTOWi, Aircraft)
    return np.power((CDpCurl*Fprop+theta2)/theta3, 2/3)/np.power(CL_eq, 1/3)

def FWP(Theta2, Theta3, MTOWi, Sweep):
    
    
    return None
    


    