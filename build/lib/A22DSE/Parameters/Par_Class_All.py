# -*- coding: utf-8 -*-
"""
Created on Mon May 13 11:37:54 2019

@author: hksam
"""
#import sys
#sys.path.append('../../')
#from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import WSandTW
#from A22DSE.Models.POPS.Current.cruisecalculations import CruiseRange, CruiseTime
#from A22DSE.Models.POPS.Current.cruisecalculations import CruiseRange, CruiseTime

           
class ParAnFPLst(object):
    
    def __init__(self):
        

        self.A = None #[-]                          DUMMY VALUE
        self.e = None  #[-]                        DUMMY VALUE
        self.CD0 = None #[-]                       DUMMY VALUE
        self.S = None #[m_squared]               DUMMY VALUE
        
        #cruise parameters
        self.TtoW = None #[-]                                                                        air to fuel ratio                           by POPS
        self.Mdd = None #[-]
        self.h_cruise = 20000.
        self.M_cruise = None #[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
        self.s_cruise = None
        self.V_cruise = None
        self.t_cruise = None
        self.CL_cruise = 1.2          #[-]              DUMMY VALUE
        self.CL_max_cruise = 1.5
        self.c_j = 0.6/3600          #[s^-1]            DUMMY VALUE
        self.SFC = 16*10e-6				#[kg/N/s]          DUMMY VALUE
        self.LD = 16                 #[-]               DUMMY VALUE
        
        #takeoff parameters
        self.CL_to = 1.8					#[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
        self.CD_to = 0.1					#[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
        self.fieldlen_to = 2500 #m 
        self.rho_SL = 1.225 #[kg/m3]
        self.T_to = None			#[N]                 DUMMY
        self.Vr = 50						#[m/s]            DUMMY
        
        #landing parameters
        self.CL_land = 2.8				#[-]                       DUMMY VALUE
        self.CD_land = 0.3				#[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
        self.fieldlen_land = 2500 #m 
    
    def Get_V_cruise(self):
        return self.s_cruise/self.t_cruise
        
class ParCntrlLst(object):
    
    def __init__(self):
        self.placeholder = None
    
class ParStrucLst(object):
        
        def __init__(self):
            
            self.MTOW = None				#[kg]
            self.FW = None #[kg]                #Fuel weight
            self.N_engines = 2 #[-] 
            
            #ratios
            self.OEWratio = 1/2.47      #[-]
            self.wfratioclimb = 0.8
 
            
class ParPayloadLst(object):
    
    def __init__(self):
        self.disperRatePerTime = None
        self.airtofuel = 6 #[-]                                                                        air to fuel ratio                           by POPS
        self.m_sulphur = 10000. #[kg]                                                                  sulphur mass per flight                     by POPS           
        self.rho_sulphur = 1121 #[kg/m^3]                                                              density of solid sulphur                    by POPS
        self.rho_alu = 2700 #[kg/m^3]                                                                  density of aluminium                        by POPS
        self.dispersionrate = 8e-3 #[kg/m]
     
class ParCostLst(object):
    
    def __init__(self):
        #Cost parameters
        self.CEF8919 = 284.5/112.5 #[USD/hr]
        self.CEF7019 = 284.5/112.5+3.02 #[USD/hr]
        self.Fmat= 2.25
        self.rer = 62 #[USD/hr] CEF00/CEF89
        self.rmr = 34 #[USD/hr] CEF00/CEF89
        self.rtr = 43 #[USD/hr] CEF00/CEF89
        self.Fdiff = 1.5 #[-]
        self.Fcad = 0.8 #[-]
        self.Nrdte= 6 #[-] nr of test ac, between 2-8
        self.Nst = 2 #[-] nr of static test ac
        self.Fobs = 1 #[-]
        self.Fpror = 0.1 #[-]
        self.Ffinr = 0.05 #[-]
        self.Ftsf = 0.2 #CHECK VALUE!!!!!
        self.Cavionics = 30000000 #CHECK VALUE
        self.Nrr = 0.33 #[-]
        self.Nprogram = 150 #[-]
        self.Nrm = 11/12 #[-]
        self.tpft = 10 #[hrs]
        self.Fftoh = 4.0 #[-]
        self.FfinM = 0.10 #[-]

class ParConvLst(object):

    def __init__(self):
        
        self.ft2m = 0.3048 #[ft/m]
        self.lbs2kg = 0.453592 #[lbs/kg]
        self.mile2m = 1609.34 #[miles/meter] 
        self.gallon2L = 3.78541 #[-]
        self.kts2ms = 0.514444444 #[-]
        
class ParSensitivityAnalysis(object):
    
    def __init__(self):
        self.N_cont_lines = 10
        self.N_colours = 10
        self.X_steps = 10
        self.Y_steps = 10
        
        
        

class Aircraft(object):
            
    def __init__(self):
        # LOAD ALL classes
        self.ParPayload = ParPayloadLst()
        self.ParAnFP = ParAnFPLst()
        self.ParCntrl = ParCntrlLst()
        self.ParCostLst = ParCostLst()
        self.ParStruc = ParStrucLst()
        self.ConversTool = ParConvLst()
        self.ParSens = ParSensitivityAnalysis()
        
        
        