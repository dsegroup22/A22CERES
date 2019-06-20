# -*- coding: utf-8 -*-
"""
Created on Thu May 16 10:10:14 2019

@author: Thomas Verduyn
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May  9 15:37:22 2019

@author: hksam
"""
import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])
#from A22DSEf
from A22DSE.Models.CostModel.Current.ProdCost import (CapcMFunc, CaedMFunc, CftoMFunc, CfinMFunc,
                      CmanFunc, CproMFunc)
from A22DSE.Models.CostModel.Current.OperCost import tground, DOC, DOCdepr, DOCflt, DOClnr, DOCmaint, Coper
import numpy as np
from A22DSE.Models.CostModel.Current.Raskom import crdte
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Parameters.Par_Class_Conventional import Conv



def SummaryCost(Aircraft, Cer):
    '''INPUT: Object of class aircraft, engine cost in 2019 USD
       OUTPUT: List of the cost breakdown for acquisition & manufacturing AND
       Operations costs.
       DESCRIPTION: Prints the cost breakdown of the acquisition and 
       manufacturing and total cost.'''
    #Research and Development
    RnDC = crdte(Aircraft, ISA_model, Cer)/1e9
    
    #Acquisition and Manufacturing
    CapcM = CapcMFunc(Aircraft, ISA_model, Cer)
    CaedM = CaedMFunc(Aircraft, ISA_model)
    CftoM = CftoMFunc(Aircraft)
    CfinM = CfinMFunc(Aircraft, CaedM, CapcM, CftoM)
    Cman = CapcM + CaedM + CftoM + CfinM
    CproM = CproMFunc(Cman)
    Cacq = (Cman + CproM)/1e9
    
    ManAcqLst = np.array([CaedM, CapcM, CftoM, CfinM, CproM, Cacq])
    #Operations
    docflt=DOCflt(Aircraft,Cman)
    docmaint=DOCmaint(Aircraft,Cman)
    docdepr=DOCdepr(Aircraft,Cman)
    doclnr=DOClnr(Aircraft)[0]          #Returns direct operating costs per nm
    frt=DOClnr(Aircraft)[1]
    x=DOC(docflt,docmaint,docdepr,doclnr,frt)
    OpsCost=Coper(Aircraft,x)[0]/1e9

    OpsLst = np.array([docflt, docmaint, docdepr, doclnr, frt, x, OpsCost])    
    #Final Breakdown
    TotalCost = OpsCost + Cacq + RnDC
    UnitCost = (Cacq+RnDC)/Aircraft.ParPayload.fleetsize_y15*1000
    ManuCost = Cacq/Aircraft.ParPayload.fleetsize_y15*1000
    
    
    print("\nManufacturing Cost Breakdown:\n", "Airplane Production Cost: ",
          CapcM/1e6, "\nAirframe Engineering and Design Cost: ", CaedM/1e6,
          "\nProduction Flight Test Operation Cost: ", CftoM/1e6, 
          "\nCost of Financing: ", CfinM/1e6, "\n Profit of Manufacturing: ",
          CproM/1e6)
    
    
    print("\n================================in B$==========================\n"
          + "Total Acquisition Cost: ", Cacq, "\nTotal RnD cost: ", RnDC, 
          "\nEstimated Unit Cost: ", UnitCost, "\nCost per AC per year: ",\
          Coper(Conv,x)[1],"\nManufacturing Cost per AC :",ManuCost,\
          "\nTotal Operational Cost: ",OpsCost
          ," ---------------------------------------------------------------\n"
          , "Total Program Cost: ", TotalCost)
    return ManAcqLst, OpsLst
# =============================================================================
#                                     MAIN
# =============================================================================
'''Uncomment the assign statement below to see the cost breakdown'''
#TestAC = Aircraft()
#TestAC.ParStruc.MTOW = 30e3 #kg
#TestAC.ParAnFP.V_cruise   = 210  # m/s
#Cer  = 1.5e7 # USD19
#TestAC.ParCostLst.Nprogram = 150 # Number of aircraft
#TestAC.ParStruc.N_engines = 2
#CEF0019 = 1.484


#ManAcqLstConv = SummaryCost(Conv, Cer)[0]/CEF0019
#ManAcqLstCan  = SummaryCost(Can, Cer)[0]/CEF0019



