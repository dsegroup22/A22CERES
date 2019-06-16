# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 18:41:13 2019

@author: menno
"""

import os
from subprocess import Popen, PIPE, check_call, run


#os.system(r"datcom.exe C:\Users\menno\Documents\GitHub\A22CERES\A22DSE\Models\DATCOM\Current\ceres.dat")
#p= Popen(["datcom.exe"],stdin=PIPE,stdout=PIPE)    
#p.communicate(b"ceres.dat")
print(Popen(['Current\datcom.exe'],stdin=PIPE,stdout=PIPE).communicate(b'C:\Users\menno\Documents\GitHub\A22CERES\A22DSE\Models\DATCOM\Current\ceres.dat'))