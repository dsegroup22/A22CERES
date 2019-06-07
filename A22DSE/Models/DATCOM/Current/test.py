# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:27:47 2019

@author: menno
"""

a=['a','ad','d']
b=[3,344]
for i in a:
    if i=='ad':
        j= a.index(i)
        a[j]=str(b)
        
    