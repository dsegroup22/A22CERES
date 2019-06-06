# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""

import numpy as np
import os
from pathlib import Path
os.chdir(Path(__file__).parents[3])
from A22DSE.Parameters.Par_Class_Conventional import Conv

anfp=Conv.ParAnFP
Layout=Conv.ParLayoutConfig
Conversion=Conv.ConversTool
Struc=Conv.ParStruc


file=open('A22DSE\DATCOM\Current\PlotDatcom3d_CERESorig.m','r')

lines=file.readlines()

def printer(a):
    return print(lines[a]), print(len(lines[a]))
XW=round(float(Layout.x_apex_wing/Conversion.ft2m),1)
ZW=round(float(2),1)
ALIW=round(float(0),1)
XW=round(float(85),1)
ZW=round(float(31.5),1)
ALIH=round(float(0),1)
XV=round(float(60),1)
ZV=round(float(0),1)

NX=round(float(5),1)
X='[0.0,4.0,8.7,64.5,78.7]'
ZU='[0.0,1.3,2.6,2.6,2.6]'
ZL = '[0.0,-1.3,-2.6,-2.6,-0.66]'
R = '[0.0,2.3,4.6,4.6,0.33]'
S = '[0.0,27.2,38.4,38.4,0.34]'

CHRDTP_WG=round(float(anfp.c_t/Conversion.ft2m),1)
SSPN_WG = round(float(anfp.b/2/Conversion.ft2m),1)
SSPNE_WG = 0.9*SSPN_WG
CHRDR_WG = round(float(anfp.c_r/Conversion.ft2m),1)
SAVSI_WG = round(float(anfp.Sweep_LE/np.pi*180),1)
CHSTAT_WG = 0.0
TWISTA_WG = -3.0
DHDADI_WG = -2.0
TC_WG=0.12

CHRDTP_HT = round(float(Layout.c_tht/Conversion.ft2m),1)
SSPN_HT = round(float(Layout.bh/2/Conversion.ft2m*2),1)
SSPNE_HT=0.9*SSPN_HT
CHRDR_HT = round(float(Layout.c_rht/Conversion.ft2m),1)
SAVSI_HT = round(float(Layout.Sweep25ht),1)
CHSTAT_HT = 0.25
TWISTA_HT = 0.0
DHDADI_HT = 0.0

CHRDTP_VT = round(float(Layout.c_tvt/Conversion.ft2m),1)
SSPN_VT = round(float(Layout.bv/2/Conversion.ft2m*2),1)
SSPNE_VT=0.9*SSPN_VT
CHRDR_VT = round(float(Layout.c_rvt/Conversion.ft2m),1)
SAVSI_VT = round(float(Layout.Sweep25vt),1)
CHSTAT_VT = 0.25

for line in lines:
    if line[:2]=='XW':
        line='XW='+str(XW)+';\n'
    if line[:2]=='ZW':        
        line='ZW='+str(ZW)+';\n'
    if line[:4]=='ALIW':
        line='ALIW='+str(ALIW)+';\n'
    if line[:2]=='XH':        
        line='XH='+str(XW)+';\n'
    if line[:2]=='ZH':        
        line='ZH='+str(ZW)+';\n'
    if line[:4]=='ALIH':        
        line='ALIH='+str(ALIH)+';\n'
    if line[:2]=='XV':        
        line='XV='+str(XV)+';\n'
    if line[:2]=='ZV':        
        line='ZV='+str(ZV)+';\n'
    
    
    if line[:2]=='NX':
        line='NX='+str(NX)+';\n'
    if line[:1]=='X':
        line='X='+str(X)+';\n'
    if line[:2]=='ZU':
        line='ZU='+str(ZU)+';\n'
    if line[:2]=='ZL':
        line='ZL='+str(ZL)+';\n'
    if line[:1]=='R':
        line='R='+str(R)+';\n'
    if line[:1]=='S':
        line='S='+str(S)+';\n'
    
    
    if line[:9]=='CHRDTP_WG':
        line='CHRDTP_WG='+str(CHRDTP_WG)+';\n'
    if line[:8]=='SSPNE_WG':
        line='SSPNE_WG='+str(SSPNE_WG)+';\n'
    if line[:7]=='SSPN_WG':
        line='SSPN_WG='+str(SSPN_WG)+';\n'
    if line[:]=='CHRDR_WG':
        line='CHRDR_WG='+str(CHRDR_WG)+';\n'
    if line[:]=='SAVSI_WG':
        line='SAVSI_WG='+str(SAVSI_WG)+';\n'
    if line[:]=='CHSTAT_WG':
        line='CHSTAT_WG='+str(CHSTAT_WG)+';\n'
    if line[:]=='TWISTA_WG':
        line='TWISTA_WG='+str(TWISTA_WG)+';\n'
    if line[:]=='DHDADI_WG':
        line='DHDADI_WG='+str(DHDADI_WG)+';\n'
    if line[:]=='TC_WG':
        line='TC_WG='+str(TC_WG)+';\n'
    if line[:]=='CHRDTP_HT':
        line='CHRDTP_HT='+str(CHRDTP_HT)+';\n'
    if line[:]=='SSPNE_HT':
        line='SSPNE_HT='+str(SSPNE_HT)+';\n'
    if line[:]=='SSPN_HT':
        line='SSPN_HT='+str(SSPN_HT)+';\n'
    if line[:]=='CHRDR_HT':
        line='CHRDR_HT='+str(CHRDR_HT)+';\n'
    if line[:]=='SAVSI_HT':
        line='SAVSI_HT='+str(SAVSI_HT)+';\n'
    if line[:]=='CHSTAT_HT':
        line='CHSTAT_HT='+str(CHSTAT_HT)+';\n'
    if line[:]=='TWISTA_HT':
        line='TWISTA_HT='+str(TWISTA_HT)+';\n'
    if line[:]=='DHDADI_HT':
        line='DHDADI_HT='+str(DHDADI_HT)+';\n'
    if line[:]=='CHRDTP_VT':
        line='CHRDTP_VT='+str(CHRDTP_VT)+';\n'
    if line[:]=='SSPNE_VT':
        line='SSPNE_VT='+str(SSPNE_VT)+';\n'
    if line[:]=='SSPN_VT':
        line='SSPN_VT='+str(SSPN_VT)+';\n'
    if line[:]=='CHRDR_VT':
        line='CHRDR_VT='+str(CHRDR_VT)+';\n'
    if line[:]=='SAVSI_VT':
        line='SAVSI_VT='+str(SAVSI_VT)+';\n'
    if line[:]=='SAVSI_VT':
        line='SAVSI_VT='+str(SAVSI_VT)+';\n'

       
file.close()


file=open('A22DSE\DATCOM\Current\PlotDatcom3d_CERESorig.m','w')
for line in lines:
    file.write(line)
file.close()
