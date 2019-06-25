# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:50:44 2019

@author: tomhu
"""
#import numpy as np
import os


files = open("sc20010.dat", "r") 
file = files.readlines()
files.close()
heading = file[:3]
data = file[3:]

for i in range(len(data)):
    data[i] = data[i].split()
    for j in range(len(data[i])):
        data[i][j] = float(data[i][j])
        

#os.remove("AIRFOIL.dat")

f= open("sc20010.dat","w+")
for i in range(1,int(len(data)/2-1)):
    for j in range(len(data[i])):
#        print(data[i][j])
        f.write(str(data[-i-int(len(data)/2)-1][j])+"  ")
    f.write("\n")
    
for i in range(1,int(len(data)/2)):
    for j in range(len(data[i])):
#        print(data[is][j])
        f.write(str(data[i+int(len(data)/2)][j])+"  ")
    f.write("\n")
f.write(str(data[0][0])+" "+str(data[0][1]))
f.close()
dummy = input('Press Enter')