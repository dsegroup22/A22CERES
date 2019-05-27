"""This file is used to store all parameters.
The name of the parameter is called a 'key', the value of the parameter
is called a 'value'. To retrieve parameters from this dictionary 
take the following 2 steps:

Step 1: Begin code with:
        "
        import os
        from pathlib import Path
        os.chdir(Path(__file__).parents[Folders_above])
        "
        where Folders_above is the number of folders the dictionairy is above 
        your file. so if you are working in A22-DSE\AnFP\Current, Folders_above = 2
        
        if this doesn't work, use:
        "
        import sys
        sys.path.append('../')
        "
        depending on how deep your file is, use additionall '../'. So for file within 2 folders from 
        All_dic_Parameters, use sys.path.append('../../')
Step 2: import the function: "from All_dic_Parameters import Parameters as par"
        make sure that you define the right path first, because this file is
        not in the same folder as other files.
Step 3: retrieve the parameters.
        to retrieve the 'value', you need to the following:
        (dict_name).get('key'). so if you want to retrieve the value of the 
        key 'C_L', you need to write: par.get('C_L').  

To add parameters to this file, adhere to the following convention:
    
    'key' : 'value', #[unit]     full name+discription       determined by which department
    Parameters['key'] = value #[unit]     full name+discription       determined by which department

eg:
    'C_L_cruise' : 1.2, #[-]      Lift coeficient of total a/c at cruise       by AnFP     
    Parameters['C_L_cruise'] = 1.2 #[-]      Lift coeficient of total a/c at cruise       by AnFP     




"""
import sys
sys.path.append('../')
from AnFP.Current.AnFP_def_Atmosphere_T_p_rho import ISA
from POPS.Current.cruisecalculations import CruiseRange, CruiseTime
import numpy as np

Parameters={}

#atmospheric parameters at cruise
Parameters['gamma'] = 1.4 #[-]                                                                          ratio of specific heats                     by POPS
Parameters['R'] = 287.058 #[J/kg/K]                                                                     specific gas constant of air                by POPS
Parameters['g_0'] = 9.80665 #[m/s^2]                                                                    gravity at sea level                        by POPS
Parameters['h_cruise'] = 20000 #[m]                                                                     cruise altitude                             by All
Parameters['T_cruise'] = ISA(np.array([Parameters['h_cruise']]))[0] #[K]                                cruise temperature                          by POPS
Parameters['p_cruise'] = ISA(np.array([Parameters['h_cruise']]))[1] #[Pa]                               cruise ambient pressure                     by POPS
Parameters['rho_cruise'] = ISA(np.array([Parameters['h_cruise']]))[2] #[kg/m^3]                         cruise air density                          by POPS
Parameters['a_cruise'] = np.sqrt(Parameters['gamma']*Parameters['R']*Parameters['T_cruise']) #[m/s]     speed of sound at cruise altitude           by POPS

#parameters for payload dispersion
Parameters['airtofuel'] = 6 #[-]                                                                        air to fuel ratio                           by POPS
Parameters['m_sulphur'] = 10000. #[kg]                                                                  sulphur mass per flight                     by POPS
Parameters['M_cruise'] = 0.72 #[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
Parameters['rho_sulphur'] = 1121 #[kg/m^3]                                                              density of solid sulphur                    by POPS
Parameters['rho_alu'] = 2700 #[kg/m^3]                                                                  density of aluminium                        by POPS
Parameters['dispersionrate'] = 8e-3 #[kg/m]                                                             payload dispersion rate                     by POPS     


#cruise parameters
Parameters['s_cruise'] = CruiseRange(Parameters['m_sulphur'],Parameters['dispersionrate'])#[m]          cruiserange                                 by POPS              
Parameters['t_cruise'] = CruiseTime(Parameters['m_sulphur'],Parameters['dispersionrate'],Parameters['M_cruise'],Parameters['a_cruise'])#  [s]       by POPS     
Parameters['dispersionrate_pertime']= Parameters['m_sulphur']/Parameters['t_cruise']#[kg/s]            payload dispersion rate
Parameters['V_cruise'] = Parameters['M_cruise']*Parameters['a_cruise']
Parameters['C_L_cruise'] = 1.2 #[-]             DUMMY VALUE                                             Lift coeficient of total a/c at cruise      by AnFP
Parameters['c_j'] = 0.6/3600 #[s^-1]            DUMMY VALUE
Parameters['L_D'] = 16#[-]                      DUMMY VALUE

#Parameters for take-off
Parameters['CL_to']=1.8 #[-]                                                            Lift coefficient during take-off
Parameters['CD_to']=0.1 #[-]                                                            Drag coefficient during take-off
Parameters['MTOW'] = 60000 #[kg]                                                        Maximum take-off mass
Parameters['rho_SL'] = 1.225 #[kg/m3]
Parameters['T_to'] = 200000 #[N]
Parameters['Vr'] = 50 #[m/s]

#Parameters for landing
Parameters['CL_land']=2.8 #[-]                                                            Lift coefficient during take-off
Parameters['CD_land']=0.3 #[-]                                                            Drag coefficient during take-off



#Parameters for sensitivity analysis of Wto
Parameters['A'] = 0.0883 #[-] 
Parameters['B'] = 1.0383 #[-]   

#Conversion rates
Parameters['ft2m'] = 0.3048 #[ft/m]
Parameters['lbs2kg'] = 0.453592 #[lbs/kg]
Parameters['mile2m'] = 1609.34 #[miles/meter] 
Parameters['gallon2L'] = 3.78541 #[-]
Parameters['kts2ms'] = 0.514444444 #[-]

#Cost parameters
Parameters['CEF8919'] = 284.5/112.5 #[USD/hr]
Parameters['CEF7019'] = 284.5/112.5+3.02 #[USD/hr]
Parameters['Fmat']= 2.25
Parameters['rer'] = 62 #[USD/hr] CEF00/CEF89
Parameters['rmr'] = 34 #[USD/hr] CEF00/CEF89
Parameters['rtr'] = 43 #[USD/hr] CEF00/CEF89
Parameters['Fdiff'] = 1.5 #[-]
Parameters['Fcad'] = 0.8 #[-]
Parameters['Nrdte'] = 6 #[-] nr of test ac, between 2-8
Parameters['Nst'] = 2 #[-] nr of static test ac
Parameters['Fobs'] = 1 #[-]
Parameters['Fpror'] = 0.1 #[-]
Parameters['Ffinr'] = 0.05 #[-]
Parameters['Ftsf'] = 0.2 #CHECK VALUE!!!!!
Parameters['Cavionics'] =   30000000 #CHECK VALUE
Parameters['ne'] = 2    # [-]
Parameters['Nrr'] = 0.33 #[-]
Parameters['Nrm'] = 11/12 #[-]
Parameters['tpft'] = 10 #[hrs]
Parameters['Fftoh'] = 4.0 #[-]
Parameters['FfinM'] = 0.10 #[-]

#preliminary values 
Parameters['CD_0'] = 0.012
Parameters['AR'] = 13
Parameters['e'] = 0.85
Parameters['S'] = 90 
Parameters['SFC'] = 16*10e-6 #[kg/N/s]
#preliminary values during climb
Parameters['TtoW'] = 0.68 


#====================PARAMETERS FOR DIFFERENT CONCEPTS========================#

#Parameters relevant to each concept:
Parameters['OEWratio'] = 1/2.47#-
Parameters['wfratioclimb'] = 0.69 #-
Parameters['N_engines'] = 2 #[-]                                                                   Number of engines for flying wing concept              by POPS
Parameters['fieldlen_to'] = 2500 #m 
Parameters['fieldlen_land'] = 2500 #m


#Conventional Concept
Parameters['A_conv'] = 11 #[-]                                                                          Aspect ratio for conventional concept                   by POPS                    
Parameters['e_conv'] = 0.85 #[-]                                                                        Oswald efficiency factor for conventional concept       by POPS
Parameters['C_D_0_conv'] = 0.02 #[-]                                                                    Parasitic drag for conventional concept                 by POPS
Parameters['m_sulphur_conv'] = 10000 #[kg]                                                              Payload masss for conventional concept                  by POPS
Parameters['N_engines_conv'] = 2 #[-]                                                                   Number of engines for conventional concept              by POPS
Parameters['M_dd_conv'] = 0.7 #[-]                                                                      Drag divergence Mach number for conventional concept    by POPS


#   OUTPUTS CONV CONCEPT
Parameters['MTOW_conv'] = 34949.42 #kg
Parameters['S_conv'] = 220.6 #[m2]
Parameters['ff_conv'] = 0.1908722094786729 #[-]
Parameters['T_W_conv'] = 0.76041677 #[-]

#Flying Wing Concept
Parameters['A_flying'] = 5.84 #[-]                                                                      Aspect ratio for flying wing concept                   by POPS                    
Parameters['e_flying'] = 0.6226 #[-]                                                                      Oswald efficiency factor for flying wing concept       by POPS
Parameters['C_D_0_flying'] = 0.012 #[-]                                                                    Parasitic drag for flying wing concept                 by POPS
Parameters['M_dd_flying'] = 0.84 #[-]                                                                      Drag divergence Mach number for flying concept    by POPS

#   OUTPUTS BWB CONCEPT
Parameters['MTOW_conv'] = 35362.1 #kg
Parameters['S_conv'] = 320.8910631581795 #[m2]
Parameters['ff_conv'] = 0.19421131394303093 #[-]
Parameters['T_W_conv'] = 0.93050825 #[-]


