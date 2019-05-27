import numpy as np

def PrelimCG_ranges(Aircraft):
    
    #shortcuts for Aircraft parameters
    layout = Aircraft.ParLayoutConfig
    anfp = Aircraft.ParAnFP
    
    # cg arrays (EQUAL ARRAY LENGTH REQUIRED)[m]
    x_cg_over_MAC=np.array([0.15,0.35]) # Torenbeek 737 takeoff landing p295
    x_cg=layout.x_lemac+anfp.MAC*x_cg_over_MAC
    return (x_cg)

#############################################3

def PositionsLG_Tri(Aircraft):
#DESCRIPTION: This function calculates the height of the landing gear from 
#   ground to fuselage, the x locations of the nose and main lg, with x = 0
#   at the nose. and the y locations of the nose and main lg, assuming y=0
#   in the middle of the fuselage, and that the AC is symmetric
#INPUTS: 
#   array x_cg: list with 2 values, most forward x_cg and most aft
#   array y_cg: similar as for x_cg
#   array z_cg: similar as for x_cg
#   float b: wing span[m]
#   float y_loc_eng = y-location of engine
#   float x_begin_emp: location of where the empennage begins
#   float psi, rollreq, etc: constraining angles for lg positioning
#OUTPUTS:

    #shortcut for Aircraft parameters
    anfp = Aircraft.ParAnFP
    lg = Aircraft.ParClassII_LG
    layout = Aircraft.ParLayoutConfig
    y_loc_eng = layout.y_loc_eng
    #get parameters
    x_cg =layout.x_cg 
    z_cg =layout.z_cg
    x_begin_emp = layout.x_begin_emp
    h_fuselage = layout.h_fuselage
    d_nacelle_engine = layout.d_nacelle_engine
    z_cg_over_h_fus = layout.z_cg_over_h_fus
    y_nose=layout.y_nose
    e_s = lg.e_s
    
    
    #define constraining parameters 
    theta_LO = 7*(1+3/anfp.A)*np.pi/180 #[rad] liftoff requirement angle Torenbeek p351
    theta_TD = theta_LO #[rad] Torenbeek assumed that it is the same 
    psi = lg.psi #[rad] angle from parameter file
    rollreq = lg.rollreq
    prelim_tire_diam = lg.prelim_tire_diam
    
    #assume that AC is level for taxiing etc
    l_main = l_nose = prelim_tire_diam*1.1 +e_s   #length = tire + deflection + margin of 10% 

    #z_cg based on landinggear height, and 
    z_cg[0] = l_main+z_cg_over_h_fus*h_fuselage-e_s
    z_cg[1] = l_main+z_cg_over_h_fus*h_fuselage
   
    #initialisation of x_main:
    x_main = 0.
    z_cg_old = z_cg+1
    itcount = 0
    while(itcount<10 ):   
        # touchdown requirement
        x_main_min_TD=max(x_cg)+np.tan(theta_TD)*(max(z_cg)+lg.e_s)    
        
        if(x_main_min_TD> x_main):
            x_main = x_main_min_TD
    
        # nosewheel force requirement
        x_nose_min_F_n=x_main_min_TD-(x_main_min_TD-max(x_cg))/min(lg.F_n_to_W)
        x_nose_max_F_n=x_main_min_TD-(x_main_min_TD-min(x_cg))/max(lg.F_n_to_W)
        
        while(x_nose_min_F_n>x_nose_max_F_n):
            x_main_min_TD +=0.05
            x_nose_min_F_n=x_main_min_TD-(x_main_min_TD-max(x_cg))/min(lg.F_n_to_W) 
            x_nose_max_F_n=x_main_min_TD-(x_main_min_TD-min(x_cg))/max(lg.F_n_to_W) 
    
        
        x_nose=np.average([x_nose_min_F_n,x_nose_max_F_n])
        #tail slam requirement
        x_main_tailslam = x_begin_emp-l_main/np.tan(theta_TD)
        
        if( x_main_tailslam>x_main):
            x_main = x_main_tailslam
            
        # turnover requirement
        c=max(z_cg)/np.tan(psi)
        alpha=np.arcsin(c/(max(x_cg)-x_nose))
        y_main_min_turnover=np.tan(alpha)*(x_main-x_nose)
        y_main=y_main_min_turnover
        
        
        #roll angle requirement at TO and landing
        #for wing tips:
        l_main_roll_wingtips = (anfp.b/2-y_main)*np.tan(rollreq)-h_fuselage

        #for engines
        l_main_roll_eng = (y_loc_eng-y_main)*np.tan(rollreq)\
        -h_fuselage + d_nacelle_engine
        #get constraining length, multiply by 1.02 for tire deflation
        l_main = l_nose =max(l_main,l_main_roll_wingtips, l_main_roll_eng)
        
        z_cg[0] = l_main+z_cg_over_h_fus*h_fuselage-e_s
        z_cg[1] = l_main+z_cg_over_h_fus*h_fuselage
        itcount+=1
    return(l_main,l_nose, y_main,x_main,x_nose_min_F_n,x_nose_max_F_n, x_nose,y_nose,z_cg)
