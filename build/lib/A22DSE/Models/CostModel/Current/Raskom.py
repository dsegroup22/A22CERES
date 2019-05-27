# -*- coding: utf-8 -*-
"""
Created on Wed May  8 16:43:02 2019

@author: Thomas Verduyn
"""

import numpy as np
from ProdCost import *
from RoskamFuncList import Wampr, MHRManProg, MHRToolProg, MHRtoolr, MHRmanr 
from RoskamFuncList import cmat, eas
import os
from pathlib import Path
os.chdir(Path(__file__).parents[1])

from All_dic_Parameters import Parameters as par



    #MTOW in lbs
    #Vc in m/s
    #Cer in 1990 USD
def crdte(MTOW,Vc,Cer):
    #INPUT:Maximum take-off weight, cruise velocity, engine costs
    #OUTPUT:RDTE Costs
    #Description: Research, Development, Test and Evaluation costs
#    CEF=par.get('CEF19')            #Inflation between 2018-1985
    rer=par.get('rer')*par.get('CEF8919')   #Engineering dollar rate         
    rmr=par.get('rmr')*par.get('CEF8919')   #Manufacturing dollar rate
    rtr=par.get('rtr') *par.get('CEF8919')  #Tooling dollar rate
    Nrdte=par.get('Nrdte')          #Number of test ac, is between 2-8
    Fdiff=par.get('Fdiff')          #Difficulty level of design 1-1.5-2
    Fcad=par.get('Fcad')            #Cad model factor
#    CEF=par.get('CEF19')/par.get('CEF89')            #Cost expansion factor
    Nst=par.get('Nst')              #Static test ac nr
    Fobs=par.get('Fobs')            #Factor for observable characteristics
    Fpror=par.get('Fpror')          #Profit factor
    Ffinr=par.get('Ffinr')          #Finance costs
    Ftsf=par.get('Ftsf')            #Test, simulation, facility costs
    Fmat=par.get('Fmat')            #Correction factor for type of material
    cavionics= par.get('Cavionics') #costs of ac?
    cer = Cer                   #Costs per engine at 2019
    ne=par.get('ne')                #number of engines
    Nrr=par.get('Nrr')              #RDTE production rate
    Vmax=eas(Vc)                    #keas
    kg2lbs = 1/par.get('lbs2kg')
#    ms2kts = 1/par.get('kts2ms')    
    MTOW = kg2lbs * MTOW            # change from kg to lbs
    
    cear=(cer*ne+cavionics)*(Nrdte-Nst)       #Costs of engine and avionics
    cmanr=MHRmanr(MTOW,Vmax,Nrdte,Fdiff)*rmr    #Labour costs
    cmatr=cmat(MTOW,Vmax,Nrdte,Fmat)        #Material costs
    ctoolr=MHRtoolr(MTOW,Vmax,Nrdte,Nrr,Fdiff)*rtr  #Tooling costs
    cqcr=0.13*cmanr                 #Quality control costs
    
    #Engineering manhours
    mhraedr=0.0396*Wampr(MTOW)**0.791*Vmax**1.526*Nrdte**0.183*Fdiff*Fcad
    #Aerframe engineering and design costs
    caedr=mhraedr*rer              
    #Development, support and testing costs
    cdstr=0.008325*Wampr(MTOW)**0.873*Vmax**1.89*Nrdte**0.346*Fdiff\
    *par.get('CEF7019')
    #Flight test airplane costs
    cftar=cear+cmanr+cmatr+ctoolr+cqcr
#    print (np.array([cear,cmanr,cmatr,ctoolr,cqcr,cftar])*10**(-6))
    #Flight test operation costs
    cftor=0.001244*Wampr(MTOW)**1.160*Vmax**1.371*(Nrdte-Nst)**1.281*Fdiff\
    *Fobs*par.get('CEF7019')
    #Research, development, test and evaluation costs
    crdte=(caedr+cdstr+cftar+cftor)/(1-Ftsf-Fpror-Ffinr)
    return np.array([caedr, cdstr, cftar, cftor, crdte])


#print (crdte(150000,210,3*10**7)*10**(-6))
#print (crdte(150000,210,3*10**7)*100/crdte(150000,210,3*10**7)[-1])

