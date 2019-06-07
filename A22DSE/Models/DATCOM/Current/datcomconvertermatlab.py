# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""

import numpy as np
import os
from pathlib import Path
os.chdir(Path(__file__).parents[4])
from A22DSE.Parameters.Par_Class_Conventional import Conv

anfp=Conv.ParAnFP
Layout=Conv.ParLayoutConfig
Conversion=Conv.ConversTool
Struc=Conv.ParStruc


file=open('A22DSE\Models\DATCOM\Current\PlotDatcom3d_CERESorig.m','r')

lines=file.readlines()

def printer(a):
    return print(lines[a]), print(len(lines[a]))
XW=round(float(Layout.x_apex_wing/Conversion.ft2m),1)
ZW=round(float(2),1)
ALIW=round(float(0),1)
XH=round(float(85),1)
ZH=round(float(31.5),1)
ALIH=round(float(0),1)
XV=round(float(60),1)
ZV=round(float(0),1)

NX=round(float(4),1)
X='[0.0,4.0,8.7,64.5,78.7]'
ZU='[0.0,2.6,2.6,2.6]'
ZL = '[0.0,-2.6,-2.6,-0.66]'
R = '[0.0,4.6,4.6,0.33]'
S = '[0.0,38.4,38.4,0.34]'
X=np.round(np.array([0.0,Layout.l_nose,Layout.l_nose+Layout.l_cabin,Layout.l_fuselage])/Conversion.ft2m,1)
ZU=np.round(np.array([0.0,Layout.h_fuselage/2,Layout.h_fuselage/2,Layout.h_fuselage/2])/Conversion.ft2m,1)
ZL=np.round(np.array([0.0,-Layout.h_fuselage/2,-Layout.h_fuselage/2,Layout.h_fuselage/2-Layout.h_APU/2,])/Conversion.ft2m,1)
R=np.round(np.array([0.0,Layout.w_fuselage/2,Layout.w_fuselage/2,Layout.h_APU/2,])/Conversion.ft2m,1)
S=np.round(np.array([0.0,Layout.w_fuselage*Layout.h_fuselage*np.pi/4,Layout.w_fuselage*Layout.h_fuselage*np.pi/4,Layout.h_APU**2*np.pi/4,])/Conversion.ft2m**2,1)

CHRDTP_WG=round(float(anfp.c_t/Conversion.ft2m),1)
SSPN_WG = round(float(anfp.b/2/Conversion.ft2m),1)
SSPNE_WG = 0.9*SSPN_WG
CHRDR_WG = round(float(anfp.c_r/Conversion.ft2m),1)
SAVSI_WG = round(float(anfp.Sweep_LE*180/np.pi),1)
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

for line in lines[50:96]:
    if line[:2]=='XW':
        j= lines.index(line)
        lines[j]='XW='+str(XW)+';\n'   
    if line[:2]=='ZW':
        j= lines.index(line)        
        lines[j]='ZW='+str(ZW)+';\n'
    if line[:4]=='ALIW':
        j= lines.index(line)
        lines[j]='ALIW='+str(ALIW)+';\n'
    if line[:2]=='XH':
        j= lines.index(line)        
        lines[j]='XH='+str(XH)+';\n'
    if line[:2]=='ZH':
        j= lines.index(line)
        lines[j]='ZH='+str(ZH)+';\n'
    if line[:4]=='ALIH':
        j= lines.index(line)        
        lines[j]='ALIH='+str(ALIH)+';\n'
    if line[:2]=='XV':
        j= lines.index(line)        
        lines[j]='XV='+str(XV)+';\n'
    if line[:2]=='ZV':
        j= lines.index(line)        
        lines[j]='ZV='+str(ZV)+';\n'
    
    
    if line[:2]=='NX':
        j= lines.index(line)
        lines[j]='NX='+str(NX)+';\n'
    if line[:2]=='X ' or line[:2]=='X=':
        j= lines.index(line)
        lines[j]='X='+np.array2string(X,separator=',').replace(' ','')+';\n'
    if line[:2]=='ZU':
        j= lines.index(line)
        lines[j]='ZU='+np.array2string(ZU,separator=',').replace(' ','')+';\n'
    if line[:2]=='ZL':
        j= lines.index(line)
        lines[j]='ZL='+np.array2string(ZL,separator=',').replace(' ','')+';\n'
    if line[:2]=='R ' or line[:2]=='R=':
        j= lines.index(line)
        lines[j]='R='+np.array2string(R,separator=',').replace(' ','')+';\n'
    if line[:2]=='S ' or line[:2]=='S=':
        j= lines.index(line)
        lines[j]='S='+np.array2string(S,separator=',').replace(' ','')+';\n'
    
    
    if line[:9]=='CHRDTP_WG':
        j= lines.index(line)
        lines[j]='CHRDTP_WG='+str(CHRDTP_WG)+';\n'
    if line[:8]=='SSPNE_WG':
        j= lines.index(line)
        lines[j]='SSPNE_WG='+str(SSPNE_WG)+';\n'
    if line[:7]=='SSPN_WG':
        j= lines.index(line)
        lines[j]='SSPN_WG='+str(SSPN_WG)+';\n'
    if line[:8]=='CHRDR_WG':
        j= lines.index(line)
        lines[j]='CHRDR_WG='+str(CHRDR_WG)+';\n'
    if line[:8]=='SAVSI_WG':
        j= lines.index(line)
        lines[j]='SAVSI_WG='+str(SAVSI_WG)+';\n'
    if line[:9]=='CHSTAT_WG':
        j= lines.index(line)
        lines[j]='CHSTAT_WG='+str(CHSTAT_WG)+';\n'
    if line[:9]=='TWISTA_WG':
        j= lines.index(line)
        lines[j]='TWISTA_WG='+str(TWISTA_WG)+';\n'
    if line[:9]=='DHDADI_WG':
        j= lines.index(line)
        lines[j]='DHDADI_WG='+str(DHDADI_WG)+';\n'
    if line[:5]=='TC_WG':
        j= lines.index(line)
        lines[j]='TC_WG='+str(TC_WG)+';\n'
    if line[:9]=='CHRDTP_HT':
        j= lines.index(line)
        lines[j]='CHRDTP_HT='+str(CHRDTP_HT)+';\n'
    if line[:8]=='SSPNE_HT':
        j= lines.index(line)
        lines[j]='SSPNE_HT='+str(SSPNE_HT)+';\n'
    if line[:7]=='SSPN_HT':
        j= lines.index(line)
        lines[j]='SSPN_HT='+str(SSPN_HT)+';\n'
    if line[:8]=='CHRDR_HT':
        j= lines.index(line)
        lines[j]='CHRDR_HT='+str(CHRDR_HT)+';\n'
    if line[:8]=='SAVSI_HT':
        j= lines.index(line)
        lines[j]='SAVSI_HT='+str(SAVSI_HT)+';\n'
    if line[:9]=='CHSTAT_HT':
        j= lines.index(line)
        lines[j]='CHSTAT_HT='+str(CHSTAT_HT)+';\n'
    if line[:9]=='TWISTA_HT':
        j= lines.index(line)
        lines[j]='TWISTA_HT='+str(TWISTA_HT)+';\n'
    if line[:9]=='DHDADI_HT':
        j= lines.index(line)
        lines[j]='DHDADI_HT='+str(DHDADI_HT)+';\n'
    if line[:9]=='CHRDTP_VT':
        j= lines.index(line)
        lines[j]='CHRDTP_VT='+str(CHRDTP_VT)+';\n'
    if line[:8]=='SSPNE_VT':
        j= lines.index(line)
        lines[j]='SSPNE_VT='+str(SSPNE_VT)+';\n'
    if line[:7]=='SSPN_VT':
        j= lines.index(line)
        lines[j]='SSPN_VT='+str(SSPN_VT)+';\n'
    if line[:8]=='CHRDR_VT':
        j= lines.index(line)
        lines[j]='CHRDR_VT='+str(CHRDR_VT)+';\n'
    if line[:8]=='SAVSI_VT':
        j= lines.index(line)
        lines[j]='SAVSI_VT='+str(SAVSI_VT)+';\n'
    if line[:9]=='CHSTAT_VT':
        j= lines.index(line)
        lines[j]='CHSTAT_VT='+str(CHSTAT_VT)+';\n'

       
file.close()


file=open('A22DSE\Models\DATCOM\Current\PlotDatcom3d_CERES.m','w')
for line in lines:
    file.write(line)
file.close()
