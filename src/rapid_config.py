#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 13:21:20 2022

@author: Mo Cohen
"""

import iris
import subprocess
import iris.plot as iplt
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import numpy as np
import pandas as pd
import glob
from pathlib import Path


templatepath = '/exports/csce/datastore/geos/users/s1144983/psg_files/templates'

def rapid_config(daypath, cubes, day, east=36, west=108):
    
    """ For one model column:
        Extracts profiles for: pressure, temperature, water vapour, liquid cloud, ice cloud
        Calculates/defines profiles for: N2, CO2
        Reads in a template Planetary Spectrum Generator config file with empty atmosphere layers
        Writes UM model data atmospheric profiles into atmosphere layers
        Outputs a text file labelled with the array coordinates of the column for which the profile has been generated"""
    
    for cube in cubes:
        if cube.standard_name == 'air_pressure':
            air_pressure = cube[day,:,:,:].copy()
        if cube.standard_name == 'air_potential_temperature':
            potential_temp = cube[day,:,:,:].copy()
        if cube.standard_name == 'specific_humidity':
            spec_humid = cube[day,:,:,:].copy()
        if cube.standard_name == 'mass_fraction_of_cloud_ice_in_air':
            ice_cloud = cube[day,:,:,:].copy()
        if cube.standard_name == 'mass_fraction_of_cloud_liquid_water_in_air':
            liquid_cloud = cube[day,:,:,:].copy()
    # Extract the model data cubes needed
        
    p0 = iris.coords.AuxCoord(100000.0, long_name='reference_pressure', units='Pa')
    p0.convert_units(air_pressure.units)
    absolute_temp = potential_temp*((air_pressure/p0)**(287.05/1005)) # R and cp in J/kgK for 300K
    # Convert potential temperature into absolute temperature
    
    altitude = air_pressure.coord('level_height').points*1e-3
    # Extract altitude of T-P points from air pressure cube (in km)
    
    air_pressure = air_pressure.data
    limb_pressure = (np.sum(air_pressure[:,:,east],axis=1) + np.sum(air_pressure[:,:,west],axis=1))/180
    absolute_temp = absolute_temp.data
    limb_temp = (np.sum(absolute_temp[:,:,east],axis=1) + np.sum(absolute_temp[:,:,west],axis=1))/180
    vapour = (28.0134/18.01528)*np.abs(spec_humid.data) # Convert kg/kg to molecules/molecules
    limb_vapour = (np.sum(vapour[:,:,east],axis=1) + np.sum(vapour[:,:,west],axis=1))/180
    
    CO2 = np.full(limb_vapour.shape,(28.0134/44.0095)*5.94e-4) # Model has a fixed amount of CO2. Convert kg/kg to molecules/molecules
    N2 = np.ones(limb_vapour.shape) - limb_vapour - CO2 # Any gas that isn't vapour or CO2 is N2
    liquid_cloud = liquid_cloud.data
    limb_liq = (np.sum(liquid_cloud[:,:,east],axis=1) + np.sum(liquid_cloud[:,:,west],axis=1))/180
    ice_cloud = ice_cloud.data
    limb_ice = (np.sum(ice_cloud[:,:,36],axis=1) + np.sum(ice_cloud[:,:,west],axis=1))/180

    template = open(str(templatepath) + '/trape_template.txt','r')    
    list_in = template.readlines()
    list_out = list_in.copy()
    template.close()
    # Open template PSG config file that already has ProxB planetary data in it, read lines into a list
    
    for layer in range(0,38):
        line_index = 54+layer # Atmosphere layers begin at line 54 of the template
        list_in[line_index] = list_in[line_index].rstrip() # Strip \n from end of line
        list_out[line_index] = list_in[line_index] + f"{limb_pressure[layer]:.4E}" + ',' + \
        f"{limb_temp[layer]:.4E}" + ',' + f"{altitude[layer]:.4E}" + ',' + f"{N2[layer]:.4E}" + ',' + f"{limb_vapour[layer]:.4E}" + ',' + \
        f"{CO2[layer]:.4E}" + ',' + f"{limb_liq[layer]:.4E}" + ',' + f"{limb_ice[layer]:.4E}" + '\n'
        # For each atmosphere layer, add pressure, temperature, N2, H2O, CO2, liquid cloud, and ice cloud data point
        # Format in scientific notation to 4 decimal places, capital E
    print(list_out) # Print to check your list formatting matches examples
    
    with open(str(daypath) + 'day_%s.txt' %(day), 'w') as file:
        for line in list_out:
            file.write(line)
            
    file.close()
    # Write to a text file labeled with array column coordinates
    
    return(list_out)


def batch_job(parentpath, cubes, first, last): 
    
    for day in range(first,last+1):
        daypath = str(parentpath) + 'configfiles/'
        Path(str(daypath)).mkdir(exist_ok=True)
        rapid_config(daypath, cubes, day=day)
    