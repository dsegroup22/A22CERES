# -*- coding: utf-8 -*-
"""
Created on Thu May  9 08:55:35 2019

@author: hksam
"""
import numpy as np
import sys
sys.path.append('../')
from All_dic_Parameters import Parameters as par
from RoskamFuncList import Wampr, MHRManProg, MHRToolProg, MHRmanr, cmat
from RoskamFuncList import MHRtoolr, eas

def CapcMFunc(MTOW, Vmax, Nprogram, CostEngine, 
         N_Engine, N_m):
    #INPUT: TO-weight [kg], Vcruise [m/s]; #a/c produced in total; Engine cost
    #       Engine per a/c; #a/c produced to production standard
    #OUTPUT: Returns the total aircraft production cost
    #Description: Computes the total aircraft production cost which consists of
    #             the cost of avionics and engines c(e+a)r, Manufacturing labor
    #             cost (Cman_m), manufacturing material cost (Cmat_m), tooling
    #             cost (Ctool_m), and lastly quality control cost Cqc_m.
    #             Each term is first computed in year 1989 USD and afterwards
    #             converted to year 2019 USD.
    # !!! NOTE: Engine and avionics are already adjusted to 2019 USD
    # !!! N_m: airplanes built to produciotn standard
    

    Nrdte = par.get('Nrdte')                # Number of test ac, is between 2-8
    Fdiff = par.get('Fdiff')                # Difficulty level of design 1 to 2
    rmr = par.get('rmr')                    #
    Fmat = par.get('Fmat')                  #Correction factor type of material
    Rtr = par.get('rtr')                    # Tooling labor rate in $/manhr
    Nrr = par.get('Nrr')                    # RDTE production rate
    Nrm = par.get('Nrm')                    # Airplane manu. rate to prod. std
    Rtm = Rtr                               # Tooling labor rate for manufact.
    kg2lbs = 1/par.get('lbs2kg')
    ms2kts = 1/par.get('kts2ms')
    CEFLabor = par.get('CEF8919')                  # Cost expansion factor
    CEFTools = par.get('CEF7019')
    MTOW = kg2lbs * MTOW
    
    # change to EAS and kts
    Vmax = Vmax * np.sqrt(par.get('rho_cruise')/par.get('rho_SL'))*ms2kts
    
#    # convert engine cost (2019) to year 1989 USD
#    CostEngine = CostEngine / CEFTools
    
    def CmanMFunc():
        CMHRManProg = MHRManProg(MTOW, Vmax, Nprogram)*rmr # rmm == rmr
        CMHRManr = MHRmanr(MTOW, Vmax, Nrdte, Fdiff)*rmr
        return np.sum([CMHRManProg, CMHRManr])*CEFLabor
    

    def CmatMFunc():
        Cmatprogr = 37.632*Fmat*np.power(Wampr(MTOW), 0.689)*\
        np.power(Vmax, 0.624)*np.power(Nprogram, 0.792)
        Cmatr = cmat(MTOW, Vmax, Nrdte, Fmat)
        return (Cmatprogr - Cmatr)*CEFTools
 
    def CtoolM():
        CMHRtoolr = MHRtoolr(MTOW, Vmax, Nrdte, Nrr, Fdiff)
        CMHRToolProg = MHRToolProg(MTOW, Wampr, Vmax, Nprogram, Nrm)
        
        return (CMHRtoolr*Rtm + CMHRToolProg*Rtr)*CEFLabor
    
    def CqcM():
        return 0.13*CmanMFunc()
    
    def Ca(TotalProdCost):
        return np.average([5,15])/100*TotalProdCost
    
    def CeaMFunc(C_avionics):
        return (CostEngine*N_Engine + C_avionics)*N_m    
    
    SumCost_excl_av = CmanMFunc() + CmatMFunc() + CtoolM() + CqcM() + \
    CeaMFunc(0)
    C_Avionics = Ca(SumCost_excl_av) # in 2019 USD
#    print(C_Avionics/Nprogram)
    
    # Perc. for profit of production
#    Profit = 0.10
    
    return np.sum(C_Avionics+SumCost_excl_av)


def CaedMFunc(MTOW, Vmax, Nprogram):
    #INPUT
    #OUPUT
    #DESCRIPTION
    
    Nrdte = par.get('Nrdte')                # Number of test ac, is between 2-8
    Fdiff = par.get('Fdiff')                # Difficulty level of design 1 to 2
    rer = par.get('rer')                      # Engineering manhour rate
    rem = rer                               # Engineering manhour rate
    Fcad = par.get('Fcad')                    # CAD model factor
    kg2lbs = 1/par.get('lbs2kg')
    CEFLabor = par.get('CEF8919')                  # Cost expansion factor
    MTOW = kg2lbs * MTOW
    
    Vmax = eas(Vmax)
    def MHRaedProg():
        return 0.0396*Wampr(MTOW)**0.791*Vmax**1.526*Nprogram**0.183*Fdiff*Fcad
    
    def MHRaedr():    #Engineering manhours
        return 0.0396*Wampr(MTOW)**0.791*Vmax**1.526*Nrdte**0.183*Fdiff*Fcad
    #Aerframe engineering and design costs
    CMHRaedr = MHRaedr()*rer
    CMHRaedProg = MHRaedProg()*rem
    
    return np.sum([CMHRaedr, CMHRaedProg])*CEFLabor


def CftoMFunc(N_m):
    #INPUT
    #OUPUT
    #DESCRIPTION    
    
    
    tpft = par.get('tpft')
    Fftoh = par.get('Fftoh')
    COpspH = None
    
    if COpspH == None:
        return 0
    return N_m*(COpspH)*tpft*Fftoh

def CfinMFunc(CaedM, CapcM, CftoM):
    #INPUT
    #OUPUT
    #DESCRIPTION    
    
    
    FfinM = par.get('FfinM')
    return np.sum([CaedM,CapcM, CftoM])/(1-FfinM)

def CproMFunc(TotalManCost):
    #INPUT
    #OUPUT
    #DESCRIPTION
    
    PercProfit = 0.10
    return TotalManCost*PercProfit

def CmanFunc(MTOW, Vmax, Nprogram, CostEngine, N_Engine, N_m):
    
    
    
    CapcM = CapcMFunc(MTOW, Vmax, Nprogram, CostEngine, N_Engine, N_m)
    CaedM = CaedMFunc(MTOW, Vmax, Nprogram)
    CftoM = CftoMFunc(N_m)
    CfinM = CfinMFunc(CaedM, CapcM, CftoM)
    return np.sum([CapcM, CaedM, CftoM, CfinM])/10**9
