

import numpy as np

class Engine:
    def __init__(self,name, thrust, weight, SFC, cost, bpr, LPC, HPC):
        self.name = name #The engine name
        self.thrust = thrust #The engine thrust
        self.weight = weight #The engine weight
        self.SFC = SFC #The engine SFC
        self.cost = cost #The engine cost
        self.bpr = bpr #The engine bypass ratio
        self.LPC = LPC #The engine LPC
        self.HPC = HPC #The engine HPC
    

def Lowbypassafter(Aircraft, Fsl, ISA_model):
    Tamb, Pamb = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[0:2] #Calculation of ambient conditions
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2) #Calculation of total temp relative with 1D compressibility
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4) #Calculation of total temp relative with 1D compressibility
    TR = 1.0 #Throttle ratio
    if theta0 <= TR:
        F = Fsl*delta0 #Empirical formula "General Aviation Aircraft Design, Applied Methods and Procedures" page 200
    else:
        F = Fsl*delta0*(1-3.5*(theta0-TR)/(theta0))
    return F

def Lowbypass(Aircraft, Fsl, ISA_model):
    Tamb, Pamb = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4)
    TR = 1.0
    if theta0 <= TR:
        F = 0.6*Fsl*delta0 #Empirical formula "General Aviation Aircraft Design, Applied Methods and Procedures" page 200
    else:
        F = 0.6*Fsl*delta0*(1-3.8*(theta0-TR)/(theta0))
    return F

def Highbypass(Aircraft, Fsl, ISA_model):
    Tamb, Pamb = ISA_model.ISAFunc([Aircraft.ParAnFP.h_cruise])[0:2]
    theta0 = Tamb/288.15*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)
    delta0 = Pamb/101325*(1+0.4/2*Aircraft.ParAnFP.Mdd**2)**(1.4/0.4)
    TR = 1.0
    if theta0 <= TR:
        F = Fsl*delta0*(1-0.49*np.sqrt(Aircraft.ParAnFP.Mdd)) #Empirical formula "General Aviation Aircraft Design, Applied Methods and Procedures" page 200
    else:
        F = Fsl*delta0*(1-0.49*np.sqrt(Aircraft.ParAnFP.Mdd)-3*(theta0-TR)/\
                        (1.5+Aircraft.ParAnFP.Mdd))
    return F

def EngineChoice(Aircraft,ISA_model,afterburner):
    T = Aircraft.ParAnFP.TWactcruise*Aircraft.ParStruc.MTOW*9.80665 #[N]
    
    engnonaft = [Engine('F118-GE-101',75700,1429,18.63814634*10e-06,999999999999,0.9,3.5,7.7),\
                 Engine('AE3007H',36880,745.7,17.703406*10e-06,4.0,4.85,1.7,13.53),\
                 Engine('EJ200',60000,1000,22.00*10e-06,8.5,0.4,4.2,6.2),\
                 Engine('F110-GE-100',73800,1800,21.10246*10e-06,7.12,0.76,4.,7.6),\
                 Engine('F100-PW-200',65270,1467,20.39432426*10e-06,6.36,0.7,3.06,8)] #Array of engine objects describing each non A/B engine
                 
    engaft = [Engine('EJ200 A/B',90000,1000,49.00*10e-06,8.5,0.4,4.2,6.2),\
              Engine('F110-GE-100 A/B',124600,1800,55.82946266*10e-06,7.12,0.76,4.,7.6),\
              Engine('F100-PW-200 A/B',106000,1467,70.8136259*10e-06,6.36,0.7,3.06,8)]#Array of engine objects describing each A/B engine
    
    if afterburner == False: #If no afterburner
        neng = np.array([]) #Total engine weight matrix
        for i in engnonaft:
            if i.name == 'AE3007H': #For high bypass
                neng = np.append(neng,[np.ceil(T/Highbypass(Aircraft, i.thrust, ISA_model))*i.weight]) #Calculate total engine mass
            else: #The rest
                neng = np.append(neng,[np.ceil(T/Lowbypassafter(Aircraft, i.thrust, ISA_model))*i.weight]) #Calculate total engine mass
        engsel = engnonaft[np.concatenate(np.where(neng == np.amin(neng)))[0]] #Select engine with lowest total mass
        
        Aircraft.ParProp.Engine_name = engsel.name #Append aircraft stuff
        Aircraft.ParStruc.N_engines = np.amin(neng)/engsel.weight
        Aircraft.ParProp.N_engines = np.amin(neng)/engsel.weight
        Aircraft.ParProp.Engine_weight = engsel.weight
        Aircraft.ParAnFP.SFC = engsel.SFC 
        Aircraft.ParProp.Engine_cost = engsel.cost
        Aircraft.ParProp.Thrust_cruise = T
        Aircraft.ParProp.Engine_bpr = engsel.bpr
        Aircraft.ParProp.Engine_LPC = engsel.LPC
        Aircraft.ParProp.Engine_HPC = engsel.HPC
    elif afterburner == True: #For afterburner
        neng = np.array([])
        for i in engaft: #Low bypass only everything else is the same
            neng = np.append(neng,[np.ceil(T/Lowbypassafter(Aircraft, i.thrust, ISA_model))*i.weight])
        engsel = engaft[np.concatenate(np.where(neng == np.amin(neng)))[0]]
        
        Aircraft.ParProp.Engine_name = engsel.name
        Aircraft.ParStruc.N_engines = np.amin(neng)/engsel.weight
        Aircraft.ParProp.N_engines = np.amin(neng)/engsel.weight
        Aircraft.ParProp.Engine_weight = engsel.weight
        Aircraft.ParAnFP.SFC = engsel.SFC 
        Aircraft.ParProp.Engine_cost = engsel.cost
        Aircraft.ParProp.Thrust_cruise = T
        Aircraft.ParProp.Engine_bpr = engsel.bpr
        Aircraft.ParProp.Engine_LPC = engsel.LPC
        Aircraft.ParProp.Engine_HPC = engsel.HPC
    else:
        print('Specify whether you want afterburners or not in EngineChoice def')
    return ()
    #return 

