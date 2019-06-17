# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 14:33:22 2019

@author: hksam
"""

import numpy as np
        ## CO2 radiative forcing == 1.985
        ## CH4 radiative forcing == 0.507
        ## N2O radiative forcing == 0.983
        ## CO  radiative forcing == 0
        ## CO  radiative forcing == 0
        ## CFC12 radiative forcing == 0.164
        ## CFC11 radiative forcing == 0.057
        
        ## GWp
        ## CO2 == 1;1;1
        ## CO  == 0;0;0
        ## CH4 == 63;21;9
        ## NO2   == 270;290;190
        ## CFC11  == 4500; 3500; 1500
        ## CFC12 == 7100;7300;4500
        ## HCFC22 == 4100;1500;510
    
class pollutant(object):
    
    def __init__(self, name, GWPLst, RFLst):
        
#        self.name = str(name)
        self.GWP  = GWPLst
        self.RF = RFLst
        
        
        
class pollutantLst(object):
    
    def __init__(self):
        
        self.CO2 = pollutant('CO2', np.array([1,1,1]), 1.985)
        self.CO  = pollutant('CO', np.array([0,0,0]), 0)
        self.H2O = pollutant('H2O', np.array([10,4,1]), 0.18)       
        self.CH4 = pollutant('CH4', np.array([63,21,9]), 0.507)
        self.N2O = pollutant('N2O', np.array([270,290, 190]), 0.983)
#        self.CFC11 = pollutant('CFC11', np.array([4500,3500,1500]), 0.057)
#        self.CFC22 = pollutant('CFC12', np.array([4100, 1500, 510]), 0.164)
#        self.HCFC22 = pollutant('HCFC22', np.array([4100, 1500, 510]), None)
        self.H2 = pollutant('H2', np.array([0,0,0]), 0)
        self.N2 = pollutant('N2', np.array([0,0,0]), 0)
        self.O2 = pollutant('O2', np.array([0,0,0]), 0)

        
        
        
    