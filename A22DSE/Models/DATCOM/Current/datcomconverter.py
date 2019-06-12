# -*- coding: utf-8 -*-9
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""

import numpy as np
from datcomconvertermatlab import *




file=open('A22DSE\Models\DATCOM\Current\CERESorig.dat','r')

lines=file.readlines()
def printer(a):
    return print(lines[a]), print(len(lines[a]))

printer(4)
a=lines[4].split(',')[0]+','
b=lines[4].split(',')[1].split('=')[0]+'='+str(round(float(Struc.MTOW/Conversion.lbs2kg),1))+','
c=lines[4].split(',')[2]
lines[4]=a+b+c
printer(4)


printer(5)
a=lines[5].split(',')[0].split('=')[0]+'='+str(round(float(anfp.S/Conversion.ft2m**2),1))+','
b=lines[5].split(',')[1].split('=')[0]+'='+str(round(float(anfp.MAC/Conversion.ft2m),1))+','
c=lines[5].split(',')[2].split('=')[0]+'='+str(2*SSPN_WG)+'$ \n'
lines[5]=a+b+c
printer(5)


printer(6)
a=lines[6].split(',')[0].split('=')[0]+'='+str(round(float(np.average(Layout.x_cg)/Conversion.ft2m),1))+','
b=lines[6].split(',')[1].split('=')[0]+'='+str(round(float((Layout.z_cg_over_h_fus-0.5)*Layout.h_fuselage/Conversion.ft2m*2),1))+','
c=lines[6].split(',')[2].split('=')[0]+'='+str(XW)+','
d=lines[6].split(',')[3].split('=')[0]+'='+str(ZW)+','
e=lines[6].split(',')[4]+','
f=lines[6].split(',')[5].split('=')[0]+'='+str(XH)+','
g=lines[6].split(',')[6]
lines[6]=a+b+c+d+e+f+g
printer(6)

printer(7)
a=lines[7].split(',')[0].split('=')[0]+'='+str(ZH)+','
b=lines[7].split(',')[1].split('=')[0]+'='+str(ALIH)+','
c=lines[7].split(',')[2].split('=')[0]+'='+str(XV)+','
d=lines[7].split(',')[3].split('=')[0]+'='+str(ZV)+','
e=lines[7].split(',')[4]
lines[7]=a+b+c+d+e
printer(7)

printer(8)
a=lines[8].split(',')[0].split('=')[0]+'='+str(NX)+','
b=lines[8].split(',')[1]+','
c=lines[8].split(',')[2]
lines[8]=a+b+c
printer(8)


a='  X='
b=np.array2string(X,separator=',').replace(' ','').replace('[','').replace(']','')
c=', \n'
lines[9]=a+b+c


a='  ZU='
b=np.array2string(ZU,separator=',').replace(' ','').replace('[','').replace(']','')
c=', \n'
lines[10]=a+b+c

a='  ZL='
b=np.array2string(ZL,separator=',').replace(' ','').replace('[','').replace(']','')
c=', \n'
lines[11]=a+b+c

a='  S='
b=np.array2string(S,separator=',').replace(' ','').replace('[','').replace(']','')
c=', \n'
lines[12]=a+b+c

a='  P='
b=np.array2string(P,separator=',').replace(' ','').replace('[','').replace(']','')
c=', \n'
lines[13]=a+b+c

a='  R='
b=np.array2string(R,separator=',').replace(' ','').replace('[','').replace(']','')
c='$ \n'
lines[14]=a+b+c

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
c=lines[17].split(',')[2].split('=')[0]+'='+str(TWISTA_WG)+','
d=lines[17].split(',')[3].split('=')[0]+'='+str(DHDADI_WG)+','
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
c=lines[20].split(',')[2].split('=')[0]+'='+str(TWISTA_HT)+','
d=lines[20].split(',')[3].split('=')[0]+'='+str(DHDADI_HT)+','
e=lines[20].split(',')[4]
lines[20]=a+b+c+d+e
printer(20)



printer(22)
a=lines[22].split(',')[0].split('=')[0]+'='+str(CHRDR_VT)+','
b=lines[22].split(',')[1].split('=')[0]+'='+str(CHRDTP_VT)+','
c=lines[22].split(',')[2].split('=')[0]+'='+str(SSPN_VT)+','
d=lines[22].split(',')[3].split('=')[0]+'='+str(SSPNE_VT)+',\n'
lines[22]=a+b+c+d
printer(22)



printer(23)
a=lines[23].split(',')[0].split('=')[0]+'='+str(SAVSI_VT)+','
b=lines[23].split(',')[1].split('=')[0]+'='+str(CHSTAT_VT)+','
c=lines[23].split(',')[2]
lines[23]=a+b+c
printer(23)

file.close()

file=open('A22DSE\Models\DATCOM\Current\Airfoiltools.txt','r')

alines=file.readlines()

file.close()

import numpy as np

Xcs=np.array([0,0.002,0.005,0.01,0.02,0.03,0.04])
for i in range(24):
    Xcs=np.append(Xcs,Xcs[-1]+0.04)
upper=alines[3:10]+alines[13:106:4]
lower=alines[107:114]+alines[117::4]


uppers=np.array([])
for line in upper:
    uppers=np.append(uppers,float(line.split(' ')[-1].replace('\n','')))


lowers=np.array([])
for line in lower:
    lowers=np.append(lowers,float(line.split(' ')[-1].replace('\n','')))
a=' $WGSCHR TYPEIN=1.0, NPTS='+str(float(len(Xcs)))+',\n'
b=' XCORD= 0.0, '+np.array2string(Xcs[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
c=' YUPPER= 0.0, '+np.array2string(uppers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
d=' YLOWER= 0.0, '+np.array2string(lowers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+'$\n'
liness=[a,b,c,d]
linesss=lines[:15]+liness+lines[16:]
file=open('A22DSE\Models\DATCOM\Current\CERES.dat','w')
for line in linesss:
    file.write(line)
file.close()
