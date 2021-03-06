# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:43:02 2019

@author: Thomas Verduyn
"""
import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])
from A22DSE.Models.CostModel.Current.RoskamFuncList import (Wampr,MHRtoolr,\
                                                            MHRmanr) 
from A22DSE.Models.CostModel.Current.RoskamFuncList import cmat, eas
# =============================================================================
# from A22DSE.Parameters.Par_Class_Diff_Configs import Conv
# from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
# from A22DSE.Parameters.Par_Class_All import Aircraft
# =============================================================================


    #MTOW in lbs
    #Vc in m/s
    #Cer in 1990 USD
def crdte(Aircraft, ISA_module, Cer):
    #INPUT:Maximum take-off weight, cruise velocity, engine costs
    #OUTPUT:RDTE Costs
    #Description: Research, Development, Test and Evaluation costs
    
#    AnFP = Aircraft.ParAnFP
    par = Aircraft.ParCostLst
    Convers = Aircraft.ConversTool      # for ease of re-engineering code
    Struct = Aircraft.ParStruc
    Prop = Aircraft.ParProp
    
#    CEF=par.get('CEF19')            #Inflation between 2019-1985
    rer=par.rer*par.CEF8919   #Engineering dollar rate         
    rmr=par.rmr*par.CEF8919   #Manufacturing dollar rate
    rtr=par.rtr*par.CEF8919  #Tooling dollar rate
    CEF7019 = par.CEF7019
    Nrdte=par.Nrdte          #Number of test ac, is between 2-8
    Fdiff=par.Fdiff          #Difficulty level of design 1-1.5-2
    Fcad=par.Fcad            #Cad model factor
#    CEF=parCEF19')/parCEF89')            #Cost expansion factor
    Nst=par.Nst              #Static test ac nr
    Fobs=par.Fobs            #Factor for observable characteristics
    Fpror=par.Fpror          #Profit factor
    Ffinr=par.Ffinr          #Finance costs
    Ftsf=par.Ftsf            #Test, simulation, facility costs
    Fmat=par.Fmat            #Correction factor for type of material
    cavionics= par.Cavionics #costs of ac?
    cer = Cer                  #Costs per engine at 2019
    ne = Prop.N_engines                      #number of engines
    Nrr= par.Nrr              #RDTE production rate
    Vmax=eas(Aircraft, ISA_module)              #keas
    kg2lbs = 1/Convers.lbs2kg
#    ms2kts = 1/parkts2ms')    
    MTOW = kg2lbs * Struct.MTOW            # change from kg to lbs
    
    cear=(cer*ne+cavionics)*(Nrdte-Nst)       #Costs of engine and avionics
    cmanr=MHRmanr(MTOW,Vmax,Nrdte,Fdiff)*rmr    #Labour costs
    cmatr=cmat(MTOW,Vmax,Nrdte,Fmat, CEF7019)        #Material costs
    ctoolr=MHRtoolr(MTOW,Vmax,Nrdte,Nrr,Fdiff)*rtr  #Tooling costs
    cqcr=0.13*cmanr                 #Quality control costs
    
    #Engineering manhours
    mhraedr=0.0396*Wampr(MTOW)**0.791*Vmax**1.526*Nrdte**0.183*Fdiff*Fcad
    #Aerframe engineering and design costs
    caedr=mhraedr*rer              
    #Development, support and testing costs
    cdstr=0.008325*Wampr(MTOW)**0.873*Vmax**1.89*Nrdte**0.346*Fdiff\
    *par.CEF7019
    #Flight test airplane costs
    cftar=cear+cmanr+cmatr+ctoolr+cqcr
#    print (np.array([cear,cmanr,cmatr,ctoolr,cqcr,cftar])*10**(-6))
    #Flight test operation costs
    cftor=0.001244*Wampr(MTOW)**1.160*Vmax**1.371*(Nrdte-Nst)**1.281*Fdiff\
    *Fobs*par.CEF7019
    #Research, development, test and evaluation costs
    crdte=(caedr+cdstr+cftar+cftor)/(1-Ftsf-Fpror-Ffinr)
    return crdte
#    return np.array([caedr, cdstr, cftar, cftor, crdte])


#print (crdte(Conv,ISA_model,Conv.ParCostLst.Cengine))




