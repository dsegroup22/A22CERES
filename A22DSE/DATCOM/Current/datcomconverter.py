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

file=open('A22DSE\DATCOM\Current\CERES.dat','r+')

lines=file.readlines()

#def printer(a):
#    return print(lines[a]), print(len(lines[a]))
#printer(5)
#a=lines[5].split(',')[0].split('=')[0]+'='+str(round(anfp.S/Conversion.ft2m**2,1))+','
#b=lines[5].split(',')[1].split('=')[0]+'='+str(round(anfp.MAC/Conversion.ft2m,1))+','
#c=lines[5].split(',')[2].split('=')[0]+'='+str(round(anfp.b/Conversion.ft2m,1))+'$ \n'
#lines[5]=a+b+c
#printer(5)
#
#
#printer(6)
#a=lines[6].split(',')[0].split('=')[0]+'='+str(round(np.average(Layout.x_cg)/Conversion.ft2m**2,1))+','
#b=lines[6].split(',')[1].split('=')[0]+'='+str(round((Layout.z_cg_over_h_fus-0.5)*Layout.h_fuselage/Conversion.ft2m**2,1))+','
#c=lines[6].split(',')[2].split('=')[0]+'='+str(round(Layout.x_apex_wing/Conversion.ft2m**2,1))+','
#d=lines[6].split(',')[3]+','
#e=lines[6].split(',')[4]+','
#f=lines[6].split(',')[5]+','
#g=lines[6].split(',')[6]+','
#lines[6]=a+b+c+d+e+f+g
#printer(6)
#
#printer(16)
#a=lines[16].split(',')[0].split('=')[0]+'='+str(round(anfp.c_r/Conversion.ft2m**2,1))+','
#b=lines[16].split(',')[1].split('=')[0]+'='+str(round(anfp.c_t/Conversion.ft2m**2,1))+','
#c=lines[16].split(',')[2].split('=')[0]+'='+str(round(anfp.b/2/Conversion.ft2m**2,1))+','
#d=lines[16].split(',')[3].split('=')[0]+'='+str(round(anfp.b/2*0.9/Conversion.ft2m**2,1))+','
#lines[16]=a+b+c+d
#printer(16)
#
#printer(17)
#a=lines[17].split(',')[0].split('=')[0]+'='+str(round(anfp.Sweep_LE/np.pi*180,1))+','
#b=lines[17].split(',')[1].split('=')[0]+'='+str(0.0)+','
#c=lines[17].split(',')[2]+','
#d=lines[17].split(',')[3]+','
#e=lines[17].split(',')[4]+','
#lines[17]=a+b+c+d+e
#printer(17)
#
#printer()
#a=lines[16].split(',')[0].split('=')[0]+'='+str(round(anfp.c_r/Conversion.ft2m**2,1))+','
#b=lines[16].split(',')[1].split('=')[0]+'='+str(round(anfp.c_t/Conversion.ft2m**2,1))+','
#c=lines[16].split(',')[2].split('=')[0]+'='+str(round(anfp.b/2/Conversion.ft2m**2,1))+','
#d=lines[16].split(',')[3].split('=')[0]+'='+str(round(anfp.b/2*0.9/Conversion.ft2m**2,1))+','
#lines[16]=a+b+c+d
#printer()
#
#
#
#printer(20)
#a=lines[20].split(',')[0].split('=')[0]+'='+str(round(Layout.sweepLEht/np.pi*180,1))+','
#b=lines[20].split(',')[1].split('=')[0]+'='+str(0.0)+','
#c=lines[20].split(',')[2]+','
#d=lines[20].split(',')[3]+','
#e=lines[20].split(',')[4]+','
#f=lines[20].split(',')[5]+','
#printer(20)
#

file.close()
