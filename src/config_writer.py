#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 10:05:06 2021

@author: Mo Cohen

Pipeline for post-processing UM output data.
- Collects, organises, and outputs config file data for NASA's Planetary Spectrum Generator

Model: University of Exeter Stand Alone model of Proxima Centauri b, UM vn11.8
"""

import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import numpy as np

def profiles(cubes, coords=(-1,45,36)):
    
    for cube in cubes:
        if cube.standard_name == 'air_pressure':
            air_pressure = cube.copy()
        if cube.standard_name == 'air_potential_temperature':
            potential_temp = cube.copy()
        if cube.standard_name == 'specific_humidity':
            spec_humid = cube.copy()
        if cube.standard_name == 'mass_fraction_of_cloud_ice_in_air':
            ice_cloud = cube.copy()
        if cube.standard_name == 'mass_fraction_of_cloud_liquid_water_in_air':
            liquid_cloud = cube.copy()
            
    p0 = iris.coords.AuxCoord(100000.0, long_name='reference_pressure', units='Pa')
    p0.convert_units(air_pressure.units)
    absolute_temp = potential_temp*((air_pressure/p0)**(287.05/1005)) # R and cp in J/kgK for 300K
    
    converted_pressure = air_pressure.data*1e-5
    absolute_temp = absolute_temp.data
    vapour = (28.0134/18.01528)*spec_humid.data
    CO2 = np.full(vapour.shape,(28.0134/44.0095)*5.94e-4)
    N2 = np.ones(vapour.shape) - vapour - CO2
    liquid_cloud = liquid_cloud.data
    ice_cloud = ice_cloud.data
    
    np.set_printoptions(precision=4, formatter={'float': lambda x: format(x, '.4E')})
    
    print('Air pressure (bar): ' + str(converted_pressure[coords[0],:,coords[1],coords[2]]))
    print('Air temperature (K): ' +str(absolute_temp[coords[0],:,coords[1],coords[2]]))
    print('N2 (molecules/molecules): ' + str(N2[coords[0],:,coords[1],coords[2]]))
    print('Water vapour (molecules/molecules): '+ str(vapour[coords[0],:,coords[1],coords[2]]))
    print('CO2 (molecules/molecules): ' + str(CO2[coords[0],:,coords[1],coords[2]]))
    print('Liquid cloud (kg/kg): ' + str(liquid_cloud[coords[0],:,coords[1],coords[2]]))
    print('Ice cloud (kg/kg): ' + str(ice_cloud[coords[0],:,coords[1],coords[2]]))

                                                

                                                  