# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 16:53:41 2019

@author: lujingyi
"""

def fuselagereq(Conv):
    l_tail = max(Conv.ParLayoutConfig.xvt, Conv.ParLayoutConfig.xht)
    f_lreq = Conv.ParLayoutConfig.x_lemac+Conv.ParLayoutConfig.x_oe*Conv.ParAnFP.MAC+l_tail
    return(f_lreq)
    
def fusreq(Conv):
    x_cg_aft = Conv.ParLayoutConfig.x_cg[1]
    lt = Conv.ParLayoutConfig.xht
    lf = x_cg_aft + lt 
    
    return lf