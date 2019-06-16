# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:38:38 2019

@author: menno
"""

import numpy as np
import os
from subprocess import Popen, PIPE
from pathlib import Path
os.chdir(Path(__file__).parents[4])
#from A22DSE.Parameters.Par_Class_Conventional import Conv


def PrintMatlab(Aircraft):
    
    
    anfp=Aircraft.ParAnFP
    Layout=Aircraft.ParLayoutConfig
    Conversion=Aircraft.ConversTool
    Struc=Aircraft.ParStruc

    file=open('A22DSE\Models\DATCOM\Current\PlotDatcom3d_CERESorig.m','r')
    
    lines=file.readlines()
    
    
    XW=round(float(Layout.x_apex_wing/Conversion.ft2m),1)
    ZW=round(float(Layout.h_fuselage/2/Conversion.ft2m),1)
    ALIW=round(float(0),1)
    XH=round(float(Layout.x_apex_ht/Conversion.ft2m),1)
    
    ALIH=round(float(0),1)
    XV=round(float(Layout.x_apex_vt/Conversion.ft2m),1)
    ZV=round(float(0),1)
    
    NX=round(float(4),1)
    #X='[0.0,4.0,8.7,64.5,78.7]'
    #ZU='[0.0,2.6,2.6,2.6]'
    #ZL = '[0.0,-2.6,-2.6,-0.66]'
    #R = '[0.0,4.6,4.6,0.33]'
    #S = '[0.0,38.4,38.4,0.34]'
    X=np.round(np.array([0.0,Layout.l_nose,Layout.l_nose+Layout.l_cabin,Layout.l_fuselage])/Conversion.ft2m,1)
    ZU=np.round(np.array([0.0,Layout.h_fuselage/2,Layout.h_fuselage/2,Layout.h_fuselage/2])/Conversion.ft2m,1)
    ZL=np.round(np.array([0.0,-Layout.h_fuselage/2,-Layout.h_fuselage/2,Layout.h_fuselage/2-Layout.h_APU/2,])/Conversion.ft2m,1)
    R=np.round(np.array([0.0,Layout.w_fuselage/2,Layout.w_fuselage/2,Layout.h_APU/2])/Conversion.ft2m,1)
    S=np.round(np.array([0.0,Layout.w_fuselage*Layout.h_fuselage*np.pi/4,Layout.w_fuselage*Layout.h_fuselage*np.pi/4,Layout.h_APU**2*np.pi/4,])/Conversion.ft2m**2,1)
    h=((Layout.w_fuselage-Layout.h_fuselage)/(Layout.w_fuselage-Layout.h_fuselage))**2
    P=np.round(np.array([0.0,np.pi*(Layout.h_fuselage+Layout.w_fuselage)/2*(1+3*h/(10+np.sqrt(4-3*h))),\
                             np.pi*(Layout.h_fuselage+Layout.w_fuselage)/2*(1+3*h/(10+np.sqrt(4-3*h))),Layout.h_APU*np.pi])/Conversion.ft2m,1)
    CHRDTP_WG=round(float(anfp.c_t/Conversion.ft2m),1)
    SSPN_WG = round(float(anfp.b/2/Conversion.ft2m),1)
    SSPNE_WG = 0.9*SSPN_WG
    CHRDR_WG = round(float(anfp.c_r/Conversion.ft2m),1)
    SAVSI_WG = round(float(anfp.Sweep_LE*180/np.pi),1)
    CHSTAT_WG = 0.0
    TWISTA_WG = round(float(Aircraft.ParAnFP.twwing),10)
    DHDADI_WG = round(float(Aircraft.ParAnFP.dhwing),10)
    TC_WG=0.12
    
    CHRDTP_HT = round(float(Layout.c_tht/Conversion.ft2m),1)
    SSPN_HT = round(float(Layout.bh/2/Conversion.ft2m*2),1)
    SSPNE_HT=0.9*SSPN_HT
    CHRDR_HT = round(float(Layout.c_rht/Conversion.ft2m),1)
    SAVSI_HT = round(float(Layout.sweep25ht),1)
    CHSTAT_HT = 0.25
    TWISTA_HT = round(float(Aircraft.ParAnFP.twht),10)
    DHDADI_HT = round(float(Aircraft.ParAnFP.dhht),10)
    
    CHRDTP_VT = round(float(Layout.c_tvt/Conversion.ft2m),1)
    SSPN_VT = round(float(Layout.bv/2/Conversion.ft2m*2),1)
    SSPNE_VT=0.9*SSPN_VT
    CHRDR_VT = round(float(Layout.c_rvt/Conversion.ft2m),1)
    SAVSI_VT = round(float(Layout.Sweep25vt),1)
    CHSTAT_VT = 0.25
    
    ZH=round(float(ZV+SSPN_VT),1)
    #print(DHDADI_WG,TWISTA_WG,DHDADI_HT,TWISTA_HT)
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
    return XW,ZW,ALIW,XH,ALIH,XV,ZV,NX,X,ZU,ZL,R,S,h,P,CHRDTP_WG,SSPN_WG,SSPNE_WG,\
CHRDR_WG,SAVSI_WG,CHSTAT_WG,TWISTA_WG,DHDADI_WG,TC_WG\
,CHRDTP_HT,SSPN_HT,SSPNE_HT,CHRDR_HT,SAVSI_HT,CHSTAT_HT\
,TWISTA_HT,DHDADI_HT,CHRDTP_VT,SSPN_VT,SSPNE_VT,CHRDR_VT,SAVSI_VT,CHSTAT_VT,ZH


def printer(a):
    return print(lines[a]), print(len(lines[a]))
def PrintDatcom(Aircraft):
    anfp=Aircraft.ParAnFP
    Layout=Aircraft.ParLayoutConfig
    Conversion=Aircraft.ConversTool
    Struc=Aircraft.ParStruc
    
    import numpy as np
    XW,ZW,ALIW,XH,ALIH,XV,ZV,NX,X,ZU,ZL,R,S,h,P,CHRDTP_WG,SSPN_WG,SSPNE_WG,\
CHRDR_WG,SAVSI_WG,CHSTAT_WG,TWISTA_WG,DHDADI_WG,TC_WG\
,CHRDTP_HT,SSPN_HT,SSPNE_HT,CHRDR_HT,SAVSI_HT,CHSTAT_HT\
,TWISTA_HT,DHDADI_HT,CHRDTP_VT,SSPN_VT,SSPNE_VT,CHRDR_VT,SAVSI_VT,CHSTAT_VT,ZH=PrintMatlab(Aircraft)

    file=open('A22DSE\Models\DATCOM\Current\CERESorig.dat','r')
    
    lines=file.readlines()
    
    
    #printer(4)
    a=lines[4].split(',')[0]+','
    b=lines[4].split(',')[1].split('=')[0]+'='+str(round(float(Struc.MTOW/Conversion.lbs2kg),1))+','
    c=lines[4].split(',')[2]
    lines[4]=a+b+c
    #printer(4)
    
    
    #printer(5)
    a=lines[5].split(',')[0].split('=')[0]+'='+str(round(float(anfp.S/Conversion.ft2m**2),1))+','
    b=lines[5].split(',')[1].split('=')[0]+'='+str(round(float(anfp.MAC/Conversion.ft2m),1))+','
    c=lines[5].split(',')[2].split('=')[0]+'='+str(2*SSPN_WG)+'$ \n'
    lines[5]=a+b+c
    #printer(5)
    
    
    #printer(6)
    a=lines[6].split(',')[0].split('=')[0]+'='+str(round(float(np.average(Layout.x_cg)/Conversion.ft2m),1))+','
    b=lines[6].split(',')[1].split('=')[0]+'='+str(round(float((Layout.z_cg_over_h_fus-0.5)*Layout.h_fuselage/Conversion.ft2m*2),1))+','
    c=lines[6].split(',')[2].split('=')[0]+'='+str(XW)+','
    d=lines[6].split(',')[3].split('=')[0]+'='+str(ZW)+','
    e=lines[6].split(',')[4]+','
    f=lines[6].split(',')[5].split('=')[0]+'='+str(XH)+','
    g=lines[6].split(',')[6]
    lines[6]=a+b+c+d+e+f+g
    #printer(6)
    
    #printer(7)
    a=lines[7].split(',')[0].split('=')[0]+'='+str(ZH)+','
    b=lines[7].split(',')[1].split('=')[0]+'='+str(ALIH)+','
    c=lines[7].split(',')[2].split('=')[0]+'='+str(XV)+','
    d=lines[7].split(',')[3].split('=')[0]+'='+str(ZV)+','
    e=lines[7].split(',')[4]
    lines[7]=a+b+c+d+e
    #printer(7)
    
    #printer(8)
    a=lines[8].split(',')[0].split('=')[0]+'='+str(NX)+','
    b=lines[8].split(',')[1]+','
    c=lines[8].split(',')[2]
    lines[8]=a+b+c
    #printer(8)
    
    
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
    
    #printer(16)
    a=lines[16].split(',')[0].split('=')[0]+'='+str(CHRDR_WG)+','
    b=lines[16].split(',')[1].split('=')[0]+'='+str(CHRDTP_WG)+','
    c=lines[16].split(',')[2].split('=')[0]+'='+str(SSPN_WG)+','
    d=lines[16].split(',')[3].split('=')[0]+'='+str(SSPNE_WG)+',\n'
    lines[16]=a+b+c+d
    #printer(16)
    
    #printer(17)
    a=lines[17].split(',')[0].split('=')[0]+'='+str(SAVSI_WG)+','
    b=lines[17].split(',')[1].split('=')[0]+'='+str(CHSTAT_WG)+','
    c=lines[17].split(',')[2].split('=')[0]+'='+str(TWISTA_WG)+','
    d=lines[17].split(',')[3].split('=')[0]+'='+str(DHDADI_WG)+','
    e=lines[17].split(',')[4]
    lines[17]=a+b+c+d+e
    #printer(17)
    
    #printer(19)
    a=lines[19].split(',')[0].split('=')[0]+'='+str(CHRDR_HT)+','
    b=lines[19].split(',')[1].split('=')[0]+'='+str(CHRDTP_HT)+','
    c=lines[19].split(',')[2].split('=')[0]+'='+str(SSPN_HT)+','
    d=lines[19].split(',')[3].split('=')[0]+'='+str(SSPNE_HT)+',\n'
    lines[19]=a+b+c+d
    #printer(19)
    
    
    
    #printer(20)
    a=lines[20].split(',')[0].split('=')[0]+'='+str(SAVSI_HT)+','
    b=lines[20].split(',')[1].split('=')[0]+'='+str(CHSTAT_HT)+','
    c=lines[20].split(',')[2].split('=')[0]+'='+str(TWISTA_HT)+','
    d=lines[20].split(',')[3].split('=')[0]+'='+str(DHDADI_HT)+','
    e=lines[20].split(',')[4]
    lines[20]=a+b+c+d+e
    #printer(20)
    
    
    
    #printer(22)
    a=lines[22].split(',')[0].split('=')[0]+'='+str(CHRDR_VT)+','
    b=lines[22].split(',')[1].split('=')[0]+'='+str(CHRDTP_VT)+','
    c=lines[22].split(',')[2].split('=')[0]+'='+str(SSPN_VT)+','
    d=lines[22].split(',')[3].split('=')[0]+'='+str(SSPNE_VT)+',\n'
    lines[22]=a+b+c+d
    #printer(22)
    
    
    
    #printer(23)
    a=lines[23].split(',')[0].split('=')[0]+'='+str(SAVSI_VT)+','
    b=lines[23].split(',')[1].split('=')[0]+'='+str(CHSTAT_VT)+','
    c=lines[23].split(',')[2]
    lines[23]=a+b+c
    #printer(23)
    
    file.close()
    
    file=open('A22DSE\Models\DATCOM\Current\Airfoiltools.txt','r')
    
    alines=file.readlines()
    
    file.close()
    

    
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
##########################################3
    file=open('A22DSE\Models\DATCOM\Current\Airfoiltoolsht.txt','r')
    
    alines=file.readlines()
    
    file.close()
    

    
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
    a=' $HTSCHR TYPEIN=1.0, NPTS='+str(float(len(Xcs)))+',\n'
    b=' XCORD= 0.0, '+np.array2string(Xcs[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
    c=' YUPPER= 0.0, '+np.array2string(uppers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+',\n'
    d=' YLOWER= 0.0, '+np.array2string(lowers[1:],separator=',',max_line_width=40).replace(' ','').replace(',',', ').replace(' \n','\n ').replace('[','').replace(']','')+'$\n'
    linessht=[a,b,c,d]
############################



    linesss=lines[:15]+liness+lines[16:18]+linessht+lines[19:]
    file=open('A22DSE\Models\DATCOM\Current\ceres.dat','w+')
    for line in linesss:
        file.write(line)
    file.close()
    

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def my_split(s):
    seps=['              ','             ','            ','            ','          ','         ','        ','       ','      ','     ','    ','   ','  ',' ']
    res = [s]
    for sep in seps:
        s, res = res, []
        for seq in s:
            res += seq.split(sep)
    return res

def GetDerivatives(Aircraft,speed): #'fast' or 'slow' speed input
    
    PrintDatcom(Aircraft)
    Popen(['A22DSE\Models\DATCOM\Current\datcom.exe'],stdin=PIPE,stdout=PIPE).communicate(b'C:\Users\menno\Documents\GitHub\A22CERES\A22DSE\Models\DATCOM\Current\ceres.dat')
    file=open('datcom.out','r')
    
    lines=file.readlines()
    file.close()
    k=0
    for j in range(len(lines)):
        line=lines[j]
        if 'CONDITIONS' in line:
            if k==0 or k==2:
                dataline=my_split(lines[j+8].strip(),)
                C_Ds=np.array([])
                C_Ls=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[1].isalpha():
                        if not my_split(lines[j+8+i].strip())[2].isalpha():
                            C_Ds=np.append(C_Ds,float(my_split(lines[j+8+i].strip())[1]))
                            C_Ls=np.append(C_Ls,float(my_split(lines[j+8+i].strip())[2]))

                
            
                C_D_0=np.interp(0,C_Ls,C_Ds)
                C_L_as=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[7].isalpha():
                        C_L_as=np.append(C_L_as,float(my_split(lines[j+8+i].strip())[7]))
                C_L_a=np.average(C_L_as)
                C_l_bs=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[-1].isalpha():
                        C_l_bs=np.append(C_l_bs,float(my_split(lines[j+8+i].strip())[-1]))
                C_l_b=np.average(C_l_bs)
                C_m_as=np.array([])
                for i in range(6):
                    if not my_split(lines[j+8+i].strip())[-4].isalpha():
                        C_m_as=np.append(C_m_as,float(my_split(lines[j+8+i].strip())[-4]))
                C_m_a=np.average(C_m_as)            
                       
                C_Y_b,C_n_b=np.array(dataline[9:11]).astype(float)
#                w=np.array(['C_D_0','C_L_a','C_l_b','C_m_a','C_Y_b','C_n_b'])
#                x=C_D_0,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b=np.round(np.array([C_D_0,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b])*180/np.pi,5)
                #print(C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,j)
            if k==1 or k==3:
                dataline=my_split(lines[j+9].strip(),)
                C_L_adots=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[3].isalpha():
                        C_L_adots=np.append(C_L_adots,float(my_split(lines[j+9+i].strip())[3]))
                C_L_adot=np.average(C_L_adots)
                C_m_adots=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[4].isalpha():
                        C_m_adots=np.append(C_m_adots,float(my_split(lines[j+9+i].strip())[4]))
                C_m_adot=np.average(C_m_adots)
                C_l_ps=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[5].isalpha():
                        C_l_ps=np.append(C_l_ps,float(my_split(lines[j+9+i].strip())[5]))
                C_l_p=np.average(C_l_ps)
                C_Y_ps=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[6].isalpha():
                        C_Y_ps=np.append(C_Y_ps,float(my_split(lines[j+9+i].strip())[6]))
                C_Y_p=np.average(C_Y_ps)
                C_n_ps=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[7].isalpha():
                        C_n_ps=np.append(C_n_ps,float(my_split(lines[j+9+i].strip())[7]))
                C_n_p=np.average(C_n_ps)
                C_n_rs=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[8].isalpha():
                        C_n_rs=np.append(C_n_rs,float(my_split(lines[j+9+i].strip())[8]))
                C_n_r=np.average(C_n_rs)
                C_l_rs=np.array([])
                for i in range(6):
                    if not my_split(lines[j+9+i].strip())[9].isalpha():
                        C_l_rs=np.append(C_l_rs,float(my_split(lines[j+9+i].strip())[9]))
                C_l_r=np.average(C_l_rs)
    
    
                C_l_q,C_m_q=np.array(dataline[1:3]).astype(float)
#                y=np.array(['C_L_adot','C_m_adot', 'C_l_p','C_Y_p','C_n_p','C_n_r','C_l_r','C_l_q','C_m_q'])
#                z=C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q=np.round(np.array([C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q])*180/np.pi,5)
                #print(C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q,j)

            k+=1
            if speed == 'slow' and k==2:
                break
    return C_D_0,C_L_a,C_l_b,C_m_a,C_Y_b,C_n_b,C_L_adot,C_m_adot, C_l_p,C_Y_p,C_n_p,C_n_r,C_l_r,C_l_q,C_m_q

