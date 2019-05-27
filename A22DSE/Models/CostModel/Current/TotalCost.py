import sys
sys.path.append('../../../../../')
#from A22DSEf
from A22DSE.Models.CostModel.Current.Raskom import crdte
from A22DSE.Models.CostModel.Current.ProdCost import (CmanFunc, 
                                                             CproMFunc, 
                                                             CapcMFunc)
from A22DSE.Models.CostModel.Current.OperCost import (tground, DOC, 
                                                             DOCdepr, DOCflt,
                                                             DOClnr, DOCmaint,
                                                             Coper)
import numpy as np

#from A22DSE.Parameters.Par_Class_Diff_Configs import ISA_model
#from A22DSE.Parameters.Par_Class_All import Aircraft
#from A22DSE.Parameters.Par_Class_Diff_Configs import Conv, Can


def TotalC(Aircraft, ISA_model):
    par=Aircraft.ParCostLst
    Cer=par.Cengine
    RnDCost = crdte(Aircraft, ISA_model, Cer)
    Cman=CmanFunc(Aircraft, ISA_model, Cer)
    docflt=DOCflt(Aircraft,Cman)
    docmaint=DOCmaint(Aircraft,Cman)
    docdepr=DOCdepr(Aircraft,Cman)
    doclnr=DOClnr(Aircraft)[0]          #Returns direct operating costs per nm
    frt=DOClnr(Aircraft)[1]
    Cop=Coper(Aircraft,(DOC(docflt,docmaint,docdepr,doclnr,frt)))[0]
    #print ("RnD costs=",RnDCost*1e-9)
    #print ("Manufacturing costs=",Cman*1e-9)
    #print ("Operating costs=",Cop*1e-9)
    return (sum([RnDCost+Cman+Cop])*1e-9,Cop*1e-9)

#print (TotalC(Can))
