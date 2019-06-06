

import numpy as np

class Engine:
    def __init__(self,name, thrust, weight, SFC, cost):
        self.name = name
        self.thrust = thrust
        self.weight = weight
        self.SFC = SFC
        self.cost = cost
    

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
        F = Fsl*delta0*(1-0.49*np.sqrt(Aircraft.ParAnFP.Mdd)-3*(theta0-TR)/\
                        (1.5+Aircraft.ParAnFP.Mdd))
    return F

def EngineChoice(Aircraft,ISA_model,afterburner):
    T = Aircraft.ParAnFP.TWactcruise*Aircraft.ParStruc.MTOW*9.80665 #[N]
    
    engnonaft = [Engine('F118-GE-101',75700,1429,18.63814634*10e-06,999999999999),\
                 Engine('AE3007H',36880,745.7,17.703406*10e-06,4.0),\
                 Engine('EJ200',60000,1000,22.00*10e-06,8.5),\
                 Engine('F110-GE-100',73800,1800,21.10246*10e-06,7.12),\
                 Engine('F100-PW-200',65270,1467,20.39432426*10e-06,6.36)]
                 
    engaft = [Engine('EJ200 A/B',90000,1000,49.00*10e-06,8.5),\
              Engine('F110-GE-100 A/B',124600,1800,55.82946266*10e-06,7.12),\
              Engine('F100-PW-200 A/B',106000,1467,70.8136259*10e-06,6.36)]
    
    if afterburner == False:
        neng = []
        for i in engnonaft:
            neng.append(np.ceil(T/Lowbypassafter(Aircraft, i.thrust, ISA_model))*i.weight)
        engsel = engnonaft[np.concatenate(np.where(neng == min(neng)))[0]]
        
        Aircraft.ParProp.Engine_name = engsel.name
        Aircraft.ParStruc.N_engines = min(neng)/engsel.weight
        Aircraft.ParProp.Engine_weight = engsel.weight
        Aircraft.ParAnFP.SFC = engsel.SFC 
        Aircraft.ParProp.Engine_cost = engsel.cost
    elif afterburner == True:
        neng = []
        for i in engaft:
            neng.append(np.ceil(T/Lowbypassafter(Aircraft, i.thrust, ISA_model))*i.weight)
        engsel = engnonaft[np.concatenate(np.where(neng == min(neng)))[0]]
        
        Aircraft.ParProp.Engine_name = engsel.name
        Aircraft.ParStruc.N_engines = min(neng)/engsel.weight
        Aircraft.ParProp.Engine_weight = engsel.weight
        Aircraft.ParAnFP.SFC = engsel.SFC 
        Aircraft.ParProp.Engine_cost = engsel.cost
    else:
        print('Specify whether you want afterburners or not in EngineChoice def')
    #return 

