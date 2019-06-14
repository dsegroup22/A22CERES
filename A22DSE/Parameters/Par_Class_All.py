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
import numpy as np
           
class ParAnFPLst(object):
    
    def __init__(self):
        
        self.Wing_config = 'high'
        self.A = None #[-]                          DUMMY VALUE
        self.e = None  #[-]                        DUMMY VALUE
        self.CD0 = None #[-]                       DUMMY VALUE
        self.S = None #[m_squared]               DUMMY VALUE
        self.dihedral = 0. #[rad]
        #cruise parameters
        self.TtoW = None #[-]                                                                        air to fuel ratio                           by POPS
        self.Mdd = None #[-]
        self.h_cruise = 20000.
        self.M_cruise = None #[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
        self.s_cruise = None
        self.V_cruise = None
        self.t_cruise = None
        self.CL_cruise = 0.6          #[-]              DUMMY VALUE
        self.CL_max_cruise = 0.9
        self.c_j = 0.6/3600          #[s^-1]            DUMMY VALUE
        self.SFC = 16*10e-6				#[kg/N/s]          DUMMY VALUE
        self.LD = 16                 #[-]               DUMMY VALUE
        self.CLMAX = None #1.0326478
        #takeoff parameters
        self.CL_to = 1.03				#[-]                   DUMMY VALUE                                               cruise mach number                          by POPS
        self.CD_to = 0.1					#[-]                   DUMMY VALUE                                               cruise mach number                          by POPS
        self.fieldlen_to = 2500 #m 
        self.rho_SL = 1.225 #[kg/m3]
        self.T_to = None			#[N]                 DUMMY
        self.Vr = 50						#[m/s]            DUMMY
        self.V_max_TO = 150. #[m/s]
        #landing parameters
        self.CL_land = 1.03				#[-]                       DUMMY VALUE
        self.CD_land = 0.1				#[-]                       DUMMY VALUE                                               cruise mach number                          by POPS
        self.fieldlen_land = 2500 #m 
        
        #Operation parameters
#        self.fuelused = 2400        #[kg]  Fuel used per block DUMMY VALUE
        self.operatingyears = 15    #[years]
        self.flighttime = 4.853     #[hours]                DUMMY VALUE
        self.blockdist = 2409.831     #[Km]                    DUMMY VALUE
        
        #mAIN WING parameters
#        self.TRw = 1                 # wing taper ratio DUMMY ->>> Conv.ParAnFP.taper = correct value
#        self.Sweep25 = 18              # sweep in degrees DUMMY ->>>> Conv.ParAnFP.Sweep_25 = correct value
#        self.AR = 9                  # Aspect ratio of main wing DUMMY ->>> Conv.ParAnFP.A = correct value
        
        #Main wing airfoil parameters
#        self.ld = 90                 # L/D value for airfoil ->>>>> redefined as Conv.ParAnFP.LD
        self.Cldes = 0.56            # designed Cl where Cd is minimum
#        self.Clmax = 1.8             # DUMMY ->>>>>   Conv.ParAnFP.cl_max = correct value
#        self.Cm0 = -0.132            # self explantory DUMMY ->>>>>> Conv.ParAnFP = cm_0
        self.eta_airfoil=0.95        # airfoil effeciency raymer
        self.max_t_loc=0.37          # [t/c] location of maximum thickness airfoiltools
        self.alpha_0=-4.5/180*np.pi  # [rad] from airfoiltools Re=10^6
        self.alpha_stall=13.5/180*np.pi # [rad] from airfoiltools Re=10^6
        self.delta_Y=3.08            # [% of chord] LE sharpness value calculated from .dat file airfoiltools
        self.delta_alpha_C_L_max=2/180*np.pi   # [rad] change in alpha @ CLmax due to nonlinear stall, sweepLE = roughly 20 degrees
        self.C_L_to_C_l=0.83         # ratio of CLmax to Clmax due to sharpness, sweepLE = roughly 20 degrees
        self.delta_C_L_max_cruise=-0.35     # change in CLmax due to sharpness for Mach=0.6, sweepLE = roughly 20 degrees
        
        self.delta_C_L_max_lowspeed=0    # change in CLmax due to sharpness for Mach=0.6, sweepLE = roughly 20 degrees
    
    def Get_V_cruise(self):
        return self.s_cruise/self.t_cruise
        
class ParCntrlLst(object):
    
    def __init__(self):
        self.placeholder = None
    
class ParStrucLst(object):
        
        def __init__(self):
            
            self.MTOW = 25000				#[kg]      DUMMMY VALUE
            self.FW = None#[kg]                #Fuel weight
            self.N_engines = 2 #[-] 
            self.tail_angle = 15*np.pi/180 #DUMMY VALUE #[rad] angle of empannage wrt ground
            
            #ratios
            self.OEWratio = 0.6     #[-]
            self.wfratioclimb = 0.96
            self.fineness_c = 1.
            self.fineness_n = 1.25
            self.fineness_t = 10 #2
            self.SF         = 1.75
            self.Wf         = None
            self.Mw_Mtow= 0.185
            
            #material constants
            self.max_yield_stress = 110e6 #DUMMY VALUE, NEEDS TO BE UPDATED
class ParPayloadLst(object):
    
    def __init__(self):
        self.disperRatePerTime = None
        self.airtofuel = 6 #[-]                                                                        air to fuel ratio                           by POPS
        self.m_payload = None #[kg]                                                                  payload mass per flight                     by POPS           
        self.rho_payload = 1121 #[kg/m^3]                                                              density of payload                           by POPS
        self.rho_alu = 2700 #[kg/m^3]                                                                  density of aluminium                        by POPS
        self.t_tank = 0.003 #[m]                                                                          payload tank thickness                      by POPS
        self.dispersionrate = 8e-3 #[kg/m]
        
        
        self.TotalPayloadYear1 = 0.1e9 #kg
        self.OperationalDays = 250 #days
        self.turnaroundtime = 3600 #s  
        
class ParCostLst(object):
    
    def __init__(self):
        #Cost parameters
        self.Cengine = 15000000 #[USD]  DUMMY VALUE
        self.Cairframe = 35000000 #[USD] DUMMY VALUE
        self.Cavionics = 30000000 #CHECK VALUE
        self.acmanuy = 10 #[1/y] operational AC made per year
        self.MHRmapflt = 14 #[-] Can be anywhere from 4-14 (Roskam 2731/3020)
        self.MHRmengbl = 6
        self.CEF8919 = 284.5/112.5 #[USD/hr]
        self.CEF7019 = 284.5/112.5+3.02 #[USD/hr]
        self.Fmat= 2.25
        self.ASP=2.5e7    #DUMMY VALUE
        self.rer = 62 #[USD/hr] CEF00/CEF89
        self.rmr = 34 #[USD/hr] CEF00/CEF89
        self.rtr = 43 #[USD/hr] CEF00/CEF89
        self.spil = 60000 #[USD/y] CEF19/CEF89
        self.scpil = 45000 #[USD/y] CEF19/CEF89
        self.Cfuel = 2 #[USD/gallon] (2019)
        self.FD = 6.74 #[lbs/gallon]
        self.Fdiff = 1.5 #[-]
        self.Fcad = 0.8 #[-]
        self.Nrdte= 6 #[-] nr of test ac, between 2-8
        self.Nst = 2 #[-] nr of static test ac
        self.Coil = 15 #[USD/gallon] CEF19/CEF89
        self.Fobs = 1 #[-]
        self.Fpror = 0.1 #[-]
        self.Ffinr = 0.05 #[-]
        self.Ftsf = 0.2 #CHECK VALUE!!!!!
        self.Nrr = 0.33 #[-]
        self.Nrm = 11/12 #[-]
        self.tpft = 10 #[hrs]
        self.Fftoh = 4.0 #[-]
        self.FfinM = 0.10 #[-]
        self.Nprogram = 150 #[-]
        self.Rlap = 12 #[USD/h] CEF19/CEF89
        
class ParConvLst(object):

    def __init__(self):
        
        self.ft2m = 0.3048 #[ft/m]
        self.lbs2kg = 0.453592 #[lbs/kg]
        self.mile2m = 1609.34 #[miles/meter] 
        self.gallon2L = 3.78541 #[-]
        self.kts2ms = 0.514444444 #[-]
        self.km2nm = 0.539956803 #[-]
        self.lbf2N = 4.44822162 #[1 lbf = 4.448 N]
        self.psf2Pa = 47.88 #[1 psf = 47.88 Pa]
        
class ParClassII_CS(object):
    def __init__(self):
        """Parameters taken from Torenbeek p 283
        """
        self.ksc = 0.64
        self.conv = 0.768
        self.LE_slat = 1.2
        self.lift_dumper = 1.15
        self.flap_area = None
        
class ParClassII_LG(object):
    
    def __init__(self):
        #the following parameters are taken from Torenbeek p 282-283
        #they are parameters for the weight of lg, in pounds, so it needs to be converted.
        self.A_main =  40
        self.B_main = 0.16
        self.C_main = 0.019
        self.D_main = 1.5e-5
        
        self.A_nose = 20
        self.B_nose = 0.10
        self.C_nose = 0
        self.D_nose = 2e-6
        
        self.kuc_low_wing = 1.0
        self.kuc_high_wing = 1.08
        
        #preliminairy tire choice\height requirements
        self.prelim_N_tire_main = 8 #[-] number of tires for the main lg
        self.prelim_tire_diam = 0.25*2.54 #[m] preliminairy chosen tire height based on 8 tires for main lg
        #constraints for placements
        self.psi = 57/180*np.pi                    #[rad] turnover requirement angle from Torenbeek p353
        self.F_n_to_W=np.array([0.08,0.15])      # nosewheel force requirement [-] from Torenbeek p354
        self.rollreq = 8/180*np.pi              #[rad] roll requirement from Torenbeek p351
        
        #length parameters
        self.e_s=0.3                             #[m] (static schock absorber + tire) deflection
        
class ParLayoutConfig(object):

     def __init__(self):
         
         self.x_begin_emp = 18 #DUMMY VALUE #[m] xlocation of where the empenage starts
         self.y_begin_aileron = None
         self.h_fuselage = 1 #DUMMY VALUE #[m] height of fuselage (cabin)
         self.w_fuselage = 3 #DUMMY VALUE 3[m] with of fuselage (cabin)
         self.d_fuselage = None
         self.d_cockpit = None
         self.dim_cabin = None
         self.d_engine = 1.6 #DUMMY VALUE #[m] diameter of engine
         self.d_end_fus = 0.5 #[m] DUMMY VALUE
         self.d_nacelle_engine = self.d_engine*1.2
         self.x_lemac = 14 #DUMMY VALUE #[m] xlocation of LEMAC, from nose
         self.y_cg= np.array([0.,0.]) #DUMMY VALUE #[m] y_cg range (most forward & aft) 
         self.z_cg= np.array([0.,0.]) #DUMMY VALUE #[m] z_cg range (most low & high) determined in gearlocation_quad
         self.y_nose=0 # [m] front landing gear y-position for quad LG configuration
         self.z_cg_over_h_fus=0.6   #DUMMY VALUE
         self.sweepLEvt = 0.5 #DUMMY VALUE WILL BE CHANGED BY LULU IN TAIL SIZING
         
class ParProp(object):
    
    def __init__(self):
        self.Engine_weight = None
        self.psi = 0.45 # from adsee slides
        self.xf_c = -0.2 #from adsee slides
        self.h_c = 0.0451 #from adsee slides
        self.Engine_length = 1 #dummy, gets updated in EnginePlacement

class Aircraft(object):
            
    def __init__(self):
        # LOAD ALL classes
        self.ParPayload = ParPayloadLst()
        self.ParAnFP = ParAnFPLst()
        self.ParCntrl = ParCntrlLst()
        self.ParCostLst = ParCostLst()
        self.ParStruc = ParStrucLst()
        self.ParClassII_LG = ParClassII_LG()
        self.ParLayoutConfig = ParLayoutConfig()
        self.ParProp = ParProp()
        self.ConversTool = ParConvLst()
        
        
        
