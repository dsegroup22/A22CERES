# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 13:48:12 2019

@author: menno
"""

file=open('Airfoiltools.txt','r')

lines=file.readlines()

file.close()

import numpy as np

Xcs=np.array([0,0.002,0.005,0.01,0.02,0.03,0.04])
for i in range(24):
    Xcs=np.append(Xcs,Xcs[-1]+0.04)
upper=lines[3:10]+lines[13:106:4]
lower=lines[107:114]+lines[117::4]


uppers=np.array([])
for line in upper:
    uppers=np.append(uppers,float(line.split(' ')[-1].replace('\n','')))


lowers=np.array([])
for line in lower:
    lowers=np.append(lowers,float(line.split(' ')[-1].replace('\n','')))
a=' $WGSCHR TYPEIN=1.0, NPTS=31.0,\n'
b=' XCORD= 0.0, '+np.array2string(Xcs[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
c=' YUPPER= 0.0, '+np.array2string(uppers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
d=' YLOWER= 0.0, '+np.array2string(lowers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+'$'
liness=[a,b,c,d]

file=open('Goodcoordinates.txt','w')
for line in liness:
    file.write(line)
file.close()