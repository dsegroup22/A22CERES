# -*- coding: utf-8 -*-
"""
Created on Mon May 13 15:30:54 2019

@author: Nout
"""
import sys
sys.path.append('../../')
from A22DSE.Parameters.Par_Class_All import Aircraft
from A22DSE.Models.POPS.Current.cruisecalculations import (CruiseRange,
                                                           CruiseTime)
from A22DSE.Models.AnFP.Current.InitialSizing.AnFP_Exec_initsizing import (WSandTW)
from A22DSE.Parameters.Par_Class_Atmos import Atmos

import numpy as np


# =============================================================================
#                               iSA MODEL
# =============================================================================
ISA_model = Atmos()

# ===============================CONFIGURATION 1===============================
#                             conventional aircraft
# =============================================================================

Conv = Aircraft()


#Parameters not determined from functions
Conv.ParAnFP.A = 11
Conv.ParAnFP.e = 0.85
Conv.ParAnFP.CD0 = 0.02
Conv.ParAnFP.M_cruise = 0.7
Conv.ParAnFP.Mdd = 0.7



#parameters from functions

#ANFP parameters
Conv.ParAnFP.s_cruise = CruiseRange(Conv)
Conv.ParAnFP.t_cruise = CruiseTime(Conv, ISA_model)
Conv.ParAnFP.V_cruise = Conv.ParAnFP.Get_V_cruise()
Conv.ParPayload.disperRatePerTime = (Conv.ParPayload.m_sulphur
/Conv.ParAnFP.t_cruise)
Conv.ParAnFP.S = WSandTW(False,Conv,ISA_model)[2]
Conv.ParAnFP.TtoW = WSandTW(False,Conv,ISA_model)[3]

#structures parameters
Conv.ParStruc.MTOW = WSandTW(False,Conv,ISA_model)[0]
Conv.ParStruc.FW = WSandTW(False,Conv,ISA_model)[1]

Conv.Par
 


        
# ===============================CONFIGURATION 2===============================
#Other configuration example:
BWB = Aircraft()


#Parameters not determined from functions
BWB.ParAnFP.A = 8
BWB.ParAnFP.e = 0.9
BWB.ParAnFP.CD0 = 0.014
BWB.ParAnFP.M_cruise = 0.74
BWB.ParAnFP.Mdd = 0.74

#parameters from functions
BWB.ParAnFP.s_cruise = CruiseRange(BWB)
BWB.ParAnFP.t_cruise = CruiseTime(BWB, ISA_model)
BWB.ParAnFP.V_cruise = BWB.ParAnFP.Get_V_cruise()
BWB.ParPayload.disperRatePerTime = BWB.ParPayload.m_sulphur\
/BWB.ParAnFP.t_cruise
BWB.ParAnFP.S = WSandTW(False,BWB,ISA_model)[0]
BWB.ParAnFP.TtoW = WSandTW(False,BWB,ISA_model)[4]

#hi
# =============================================================================
        