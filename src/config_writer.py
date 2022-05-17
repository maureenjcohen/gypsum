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
import subprocess
import iris.plot as iplt
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import numpy as np
import pandas as pd
import glob
from pathlib import Path


templatepath = '/exports/csce/datastore/geos/users/s1144983/psg_files/templates'


def write_config(daypath, cubes, day, coords=(-1,45,36)):
    
    """ For one model column:
        Extracts profiles for: pressure, temperature, water vapour, liquid cloud, ice cloud
        Calculates/defines profiles for: N2, CO2
        Reads in a template Planetary Spectrum Generator config file with empty atmosphere layers
        Writes UM model data atmospheric profiles into atmosphere layers
        Outputs a text file labelled with the array coordinates of the column for which the profile has been generated"""
    
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
    # Extract the model data cubes needed
        
    p0 = iris.coords.AuxCoord(100000.0, long_name='reference_pressure', units='Pa')
    p0.convert_units(air_pressure.units)
    absolute_temp = potential_temp*((air_pressure/p0)**(287.05/1005)) # R and cp in J/kgK for 300K
    # Convert potential temperature into absolute temperature
    
    altitude = air_pressure.coord('level_height').points*1e-3
    # Extract altitude of T-P points from air pressure cube (in km)
    
    converted_pressure = air_pressure[day,:,coords[1],coords[2]].data
    absolute_temp = absolute_temp[day,:,coords[1],coords[2]].data
    vapour = (28.0134/18.01528)*np.abs(spec_humid[day,:,coords[1],coords[2]].data) # Convert kg/kg to molecules/molecules
    # Extract the numpy array for only the column we are looking at (much faster than extracting the full array!)
    
    CO2 = np.full(vapour.shape,(28.0134/44.0095)*5.94e-4) # Model has a fixed amount of CO2. Convert kg/kg to molecules/molecules
    N2 = np.ones(vapour.shape) - vapour - CO2 # Any gas that isn't vapour or CO2 is N2
    liquid_cloud = liquid_cloud[day,:,coords[1],coords[2]].data
    ice_cloud = ice_cloud[day,:,coords[1],coords[2]].data

    template = open(str(templatepath) + '/trape_template.txt','r')    
    list_in = template.readlines()
    list_out = list_in.copy()
    template.close()
    # Open template PSG config file that already has ProxB planetary data in it, read lines into a list
    
    for layer in range(0,38):
        line_index = 55+layer # Atmosphere layers begin at line 55 of the template
        list_in[line_index] = list_in[line_index].rstrip() # Strip \n from end of line
        list_out[line_index] = list_in[line_index] + f"{converted_pressure[layer]:.4E}" + ',' + \
        f"{absolute_temp[layer]:.4E}" + ',' + f"{altitude[layer]:.4E}" + ',' + f"{N2[layer]:.4E}" + ',' + f"{vapour[layer]:.4E}" + ',' + \
        f"{CO2[layer]:.4E}" + ',' + f"{liquid_cloud[layer]:.4E}" + ',' + f"{ice_cloud[layer]:.4E}" + '\n'
        # For each atmosphere layer, add pressure, temperature, N2, H2O, CO2, liquid cloud, and ice cloud data point
        # Format in scientific notation to 4 decimal places, capital E
#    print(list_out) # Print to check your list formatting matches examples
    
    with open(str(daypath) + 'configfiles/config_%s_%s.txt' %(coords[1], coords[2]), 'w') as file:
        for line in list_out:
            file.write(line)
            
    file.close()
    # Write to a text file labeled with array column coordinates
    
    return(list_out)
    

def day_generator(daypath, cubes, day=-1):

    """ Write PSG config files for every column on the limb
        These can be put through the PSG and the output averaged to get the final spectrum """

    Path(str(daypath)+'configfiles/').mkdir(exist_ok=True)
    Path(str(daypath)+'spectra/').mkdir(exist_ok=True)
    Path(str(daypath)+'plots/').mkdir(exist_ok=True)
    Path(str(daypath)+'output/').mkdir(exist_ok=True)
        
    for latitude in range(0,90):
        east_config = write_config(daypath, cubes, day, coords=(-1, latitude, 36))
        # east_filename = str(daypath) + 'configfiles/config_%s_36.txt' %(latitude)
        # east_cmd = 'curl -d type=all -d whdr=y --data-urlencode file@%s https://psg.gsfc.nasa.gov/api.php' %(east_filename)
        # with open(str(daypath) + 'spectra/trn_%s_36.txt' %(latitude), 'w') as file:
        #     subprocess.run(east_cmd, shell=True, stdout=file)
        # file.close()
        
        west_config = write_config(daypath, cubes, day, coords=(-1, latitude, 108))
        # west_filename = str(daypath) + 'configfiles/config_%s_108.txt' %(latitude)
        # west_cmd = 'curl -d type=all -d whdr=y --data-urlencode file@%s https://psg.gsfc.nasa.gov/api.php' %(west_filename)
        # with open(str(daypath) + 'spectra/trn_%s_108.txt' %(latitude), 'w') as file:
        #     subprocess.run(west_cmd, shell=True, stdout=file)
        # file.close()
        print('Up to latitude: ' + str(latitude))
            

def batch_job(parentpath, cubes, first, last): 
    
    for day in range(first,last+1):
        daypath = str(parentpath) + 'trap_day%s/' %(day)
        Path(str(daypath)).mkdir(exist_ok=True)
        day_generator(daypath, cubes, day=day)
#        plot_transitdepth(daypath, day=day)
        
                                                  