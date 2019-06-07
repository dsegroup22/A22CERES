# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""

import numpy as np
from datcomconvertermatlab import *




file=open('A22DSE\DATCOM\Current\CERESorig.dat','r')

lines=file.readlines()

printer(5)
a=lines[5].split(',')[0].split('=')[0]+'='+str(round(float(anfp.S/Conversion.ft2m**2),1))+','
b=lines[5].split(',')[1].split('=')[0]+'='+str(round(float(anfp.MAC/Conversion.ft2m),1))+','
c=lines[5].split(',')[2].split('=')[0]+'='+str(round(float(anfp.b/Conversion.ft2m),1))+'$ \n'
lines[5]=a+b+c
printer(5)


printer(6)
a=lines[6].split(',')[0].split('=')[0]+'='+str(round(float(np.average(Layout.x_cg)/Conversion.ft2m),1))+','
b=lines[6].split(',')[1].split('=')[0]+'='+str(round(float((Layout.z_cg_over_h_fus-0.5)*Layout.h_fuselage/Conversion.ft2m*2),1))+','
c=lines[6].split(',')[2].split('=')[0]+'='+str(XW)+','
d=lines[6].split(',')[3]+','
e=lines[6].split(',')[4]+','
f=lines[6].split(',')[5]+','
g=lines[6].split(',')[6]
lines[6]=a+b+c+d+e+f+g
printer(6)

printer(16)
a=lines[16].split(',')[0].split('=')[0]+'='+str(CHRDR_WG)+','
b=lines[16].split(',')[1].split('=')[0]+'='+str(CHRDTP_WG)+','
c=lines[16].split(',')[2].split('=')[0]+'='+str(SSPN_WG)+','
d=lines[16].split(',')[3].split('=')[0]+'='+str(SSPNE_WG)+',\n'
lines[16]=a+b+c+d
printer(16)

printer(17)
a=lines[17].split(',')[0].split('=')[0]+'='+str(SAVSI_WG)+','
b=lines[17].split(',')[1].split('=')[0]+'='+str(CHSTAT_WG)+','
c=lines[17].split(',')[2]+','
d=lines[17].split(',')[3]+','
e=lines[17].split(',')[4]
lines[17]=a+b+c+d+e
printer(17)

printer(19)
a=lines[19].split(',')[0].split('=')[0]+'='+str(CHRDR_HT)+','
b=lines[19].split(',')[1].split('=')[0]+'='+str(CHRDTP_HT)+','
c=lines[19].split(',')[2].split('=')[0]+'='+str(SSPN_HT)+','
d=lines[19].split(',')[3].split('=')[0]+'='+str(SSPNE_HT)+',\n'
lines[19]=a+b+c+d
printer(19)



printer(20)
a=lines[20].split(',')[0].split('=')[0]+'='+str(SAVSI_HT)+','
b=lines[20].split(',')[1].split('=')[0]+'='+str(CHSTAT_HT)+','
c=lines[20].split(',')[2]+','
d=lines[20].split(',')[3]+','
e=lines[20].split(',')[4]
lines[20]=a+b+c+d+e
printer(20)



printer(22)
a=lines[22].split(',')[0].split('=')[0]+'='+str(CHRDR_HT)+','
b=lines[22].split(',')[1].split('=')[0]+'='+str(CHRDTP_HT)+','
c=lines[22].split(',')[2].split('=')[0]+'='+str(SSPN_HT)+','
d=lines[22].split(',')[3].split('=')[0]+'='+str(SSPNE_HT)+',\n'
lines[22]=a+b+c+d
printer(22)



printer(23)
a=lines[23].split(',')[0].split('=')[0]+'='+str(SAVSI_VT)+','
b=lines[23].split(',')[1].split('=')[0]+'='+str(CHSTAT_VT)+','
c=lines[23].split(',')[2]
lines[23]=a+b+c
printer(23)

file.close()

file=open('A22DSE\DATCOM\Current\CERES.dat','w')
for line in lines:
    file.write(line)
file.close()
