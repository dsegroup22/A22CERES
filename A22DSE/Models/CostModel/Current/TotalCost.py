import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])
from A22DSE.Parameters.Par_Class_Conventional import Conv
#from A22DSEf
from A22DSE.Models.CostModel.Current.Raskom import crdte
from A22DSE.Models.CostModel.Current.ProdCost import (CmanFunc, 
                                                             CproMFunc, 
                                                             CapcMFunc)
from A22DSE.Models.CostModel.Current.OperCost import (tground, DOC, 
                                                             DOCdepr, DOCflt,
                                                             DOClnr, DOCmaint,
                                                             Coper)
from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model

import numpy as np

#from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
#from A22DSE.Parameters.Par_Class_All import Aircraft
#from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, Can


def TotalC(Aircraft, ISA_model):
    Cer=Aircraft.ParProp.Engine_cost*1e6
    RnDCost = crdte(Aircraft, ISA_model, Cer)
    #print (RnDCost)
    Cman=CmanFunc(Aircraft, ISA_model, Cer)
    docflt=DOCflt(Aircraft,Cman)
    docmaint=DOCmaint(Aircraft,Cman)
    docdepr=DOCdepr(Aircraft,Cman)
    doclnr=DOClnr(Aircraft)[0]          #Returns direct operating costs per nm
    frt=DOClnr(Aircraft)[1]
    Cop=Coper(Aircraft,(DOC(docflt,docmaint,docdepr,doclnr,frt)))[0]
    Copsy1 = Coper(Aircraft,(DOC(docflt,docmaint,docdepr,doclnr,frt)))[2]
    print ("RnD costs=",RnDCost*1e-9)
    print ("Manufacturing costs=",Cman*1e-9)
    print ("Operating costs=",Cop*1e-9)
    print('\n\n\n')
    return sum([RnDCost+Cman+Cop])*1e-9,Cop*1e-9,Copsy1

#print (TotalC(Conv,ISA_model))
