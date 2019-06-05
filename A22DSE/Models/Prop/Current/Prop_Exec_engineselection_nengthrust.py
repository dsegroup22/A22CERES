import numpy as np
import sys
sys.path.append('../../../../')

import A22DSE.Parameters.Par_Class_Diff_Configs as Conv

def Lowbypassafter(Aircraft, Fsl, ISA_model):
    Tamb, Pamb = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4)
    TR = 1.0
    if theta0 <= TR:
        F = Fsl*delta0
    else:
        F = Fsl*delta0*(1-3.5*(theta0-TR)/(theta0))
    return F

def Lowbypass(Aircraft, Fsl, ISA_model):
    Tamb, Pamb = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4)
    TR = 1.0
    if theta0 <= TR:
        F = 0.6*Fsl*delta0
    else:
        F = 0.6*Fsl*delta0*(1-3.8*(theta0-TR)/(theta0))
    return F

def Highbypass(Aircraft, Fsl, ISA_model):
    Tamb, Pamb = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4)
    TR = 1.0
    if theta0 <= TR:
        F = Fsl*delta0*(1-0.49*np.sqrt(Aircraft.ParAnFP.Mdd))
    else:
        F = Fsl*delta0*(1-0.49*np.sqrt(Aircraft.ParAnFP.Mdd)-3*(theta0-TR)/(1.5+Aircraft.ParAnFP.Mdd))
    return F

def EngineChoice(Aircraft,ISA_model,afterburner):
    T = Aircraft.ParAnFP.TWactcruise*Aircraft.ParStruc.MTOW
    if afterburner == False:
        #F118
        Fsl1 = 75700
        F1 = Lowbypass(Aircraft, Fsl1, ISA_model)
        neng1 = np.ceil(T/F1)
        #AE3007H
        Fsl2 = 36880
        F2 = Highbypass(Aircraft, Fsl2, ISA_model)
        neng2 = np.ceil(T/F2)
        if neng1 > neng2:
            Aircraft.ParProp.Engine_name = 'AE3007H'
            Aircraft.ParStruc.N_engines = neng2
            Aircraft.ParProp.Engine_weight = 745.7 #[kg]
            Aircraft.ParProp.Engine_SFC = 17.703406*10e-06 #[kg/Ns]
            Aircraft.ParProp.Engine_cost = 3.76
        else:
            Aircraft.ParProp.Engine_name = 'F118-GE-101'
            Aircraft.ParStruc.N_engines = neng1
            Aircraft.ParProp.Engine_weight = 1429 #[kg]
            Aircraft.ParProp.Engine_SFC = 18.63814634*10e-06 #[kg/Ns]
            Aircraft.ParProp.Engine_cost = 999999999999
    elif afterburner == True:
        #EJ200
        Fsl1 = 90000
        F1 = Lowbypassafter(Aircraft, Fsl1, ISA_model)
        neng1 = np.ceil(T/F1)
        #F110-GE-100
        Fsl2 = 124600
        F2 = Highbypassafter(Aircraft, Fsl2, ISA_model)
        neng2 = np.ceil(T/F2)
        #F100-PW-220
        Fsl3 = 106000
        F3 = Lowbypassafter(Aircraft, Fsl3, ISA_model)
        neng3 = np.ceil(T/F3)
        if neng1 < neng2 and neng1 < neng3:
            Aircraft.ParProp.Engine_name = 'EJ200'
            Aircraft.ParStruc.N_engines = neng2
            Aircraft.ParProp.Engine_weight = 1000 #[kg]
            Aircraft.ParProp.Engine_SFC = 49.00*10e-06 #[kg/Ns]
            Aircraft.ParProp.Engine_cost = 3.76
        elif neng2 < neng1 and neng2 < neng3:
            Aircraft.ParProp.Engine_name = 'F110-GE-100'
            Aircraft.ParStruc.N_engines = neng1
            Aircraft.ParProp.Engine_weight = 1800 #[kg]
            Aircraft.ParProp.Engine_SFC = 55.82946266*10e-06 #[kg/Ns]
            Aircraft.ParProp.Engine_cost = 999999999999
        else:
            Aircraft.ParProp.Engine_name = 'F100-PW-200'
            Aircraft.ParStruc.N_engines = neng3
            Aircraft.ParProp.Engine_weight = 1467 #[kg]
            Aircraft.ParProp.Engine_SFC = 70.8136259*10e-06 #[kg/Ns]
            Aircraft.ParProp.Engine_cost = 999999999999            
        
    else:
        print('Specify whether you want afterburners or not in EngineChoice def')
    return 

