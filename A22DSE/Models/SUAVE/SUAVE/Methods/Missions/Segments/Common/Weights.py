## @ingroup Methods-Missions-Segments-Common
# Weights.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
#  Initialize Weights
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def initialize_weights(segment):
    """ Sets the initial weight of the vehicle at the start of the segment
    
        Assumptions:
        Only used if there is an initial condition
        
        Inputs:
            segment.state.initials.conditions:
                weights.total_mass     [newtons]
            segment.state.conditions:           
                weights.total_mass     [newtons]
            
        Outputs:
            segment.state.conditions:           
                weights.total_mass     [newtons]

        Properties Used:
        N/A
                                
    """    

 
    if segment.state.initials:
        m_initial = segment.state.initials.conditions.weights.total_mass[-1,0]
        pay_initial = segment.state.initials.conditions.weights.payload_mass[-1,0]
        fuel_initial = segment.state.initials.conditions.weights.fuel_mass[-1,0]
    else:
        m_initial = segment.analyses.weights.vehicle.mass_properties.takeoff
        pay_initial = segment.analyses.weights.vehicle.mass_properties.cargo
        fuel_initial = 0

    m_current = segment.state.conditions.weights.total_mass
    pay_current = segment.state.conditions.weights.payload_mass
    fuel_current = segment.state.conditions.weights.fuel_mass
    
    
    segment.state.conditions.weights.total_mass[:,:] = m_current + (m_initial - m_current[0,0])
    
    segment.state.conditions.weights.payload_mass[:,:]  = pay_current + (pay_initial - pay_current[0,0])
    segment.state.conditions.weights.fuel_mass[:,:] = fuel_current + (fuel_initial - fuel_current[0,0])
        
    return
    
# ----------------------------------------------------------------------
#  Update Gravity
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def update_gravity(segment):
    """ Sets the gravity for each part of the mission
    
        Assumptions:
        Fixed sea level gravity, doesn't use a gravity model yet
        
        Inputs:
        segment.analyses.planet.features.sea_level_gravity [Data] 
            
        Outputs:
        state.conditions.freestream.gravity [meters/second^2]

        Properties Used:
        N/A
                                
    """      

    # unpack
    planet = segment.analyses.planet
    H      = segment.conditions.freestream.altitude
    
    # calculate
    g      = planet.features.compute_gravity(H)

    # pack
    segment.state.conditions.freestream.gravity[:,0] = g[:,0]

    return

# ----------------------------------------------------------------------
#  Update Weights
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def update_weights(segment):
    
    """ Integrate tbe mass rate to update the weights throughout a segment
    
        Assumptions:
        Only the energy network/propulsion system can change the mass
        
        Inputs:
        segment.state.conditions:
            weights.total_mass                [kilograms]
            weights.vehicle_mass_rate         [kilograms/second]
            freestream.gravity                [meters/second^2]
        segment.analyses.weights:
            mass_properties.operating_empty   [kilograms]
        segment.state.numerics.time.integrate [array]
            
        Outputs:
        segment.state.conditions:
            weights.total_mass                   [kilograms]
            frames.inertial.gravity_force_vector [kilograms]

        Properties Used:
        N/A
                                
    """          
    
    # unpack
    conditions = segment.state.conditions
    cargo      = segment.analyses.weights.mass_properties.cargo
    pay0       = conditions.weights.payload_mass[0,0]
    fuel0      = conditions.weights.fuel_mass[0,0]
    m0         = conditions.weights.total_mass[0,0]
    mdot_fuel  = conditions.weights.vehicle_mass_rate
    mdot_pay   = conditions.weights.vehicle_payload_rate*np.ones((len(conditions.weights.vehicle_mass_rate),1))
    g          = conditions.freestream.gravity
    I          = segment.state.numerics.time.integrate


    # calculate
    
    pay_deploy = np.dot(I,-mdot_pay )
    pay_deploy = np.where((pay_deploy + pay0) > 0, pay_deploy, -pay0)
    pay = pay0 + pay_deploy
    
    fuel_burnt = np.dot(I, -mdot_fuel )
    fuel = fuel0 - fuel_burnt
    
    m = m0 + fuel_burnt + pay_deploy

    # weight
    W = m*g

    # pack
    conditions.weights.payload_mass[1:,0]                = pay[1:,0]
    conditions.weights.fuel_mass[1:,0]                   = fuel[1:,0]
    conditions.weights.total_mass[1:,0]                  = m[1:,0] # don't mess with m0
    conditions.frames.inertial.gravity_force_vector[:,2] = W[:,0]

    return