#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 16:17:17 2021

@author: Mo Cohen

Pipeline for post-processing UM output data.
- Inputs spectra generated by NASA's Planetary Spectrum Generator and creates an averaged spectrum

Model: University of Exeter Stand Alone model of Proxima Centauri b, UM vn11.8
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob

def plot_absorption(path):
    
    files = glob.glob(str(path) + 'spectra/*.txt')    
    
    number_of_columns = []
    for number in range(len(files)):
        number_of_columns.append(number)
    number_of_rows = []
    for number in range(198):
        number_of_rows.append(number)
    
    wavelengths = []
    first_file = open(files[0], 'r')
    transmittances = first_file.readlines()
    transmittances = transmittances[1129:1328]
    for item in transmittances:
        datapoints = item.split('  ')
        wavelength = float(datapoints[0])
        wavelengths.append(wavelength)
    first_file.close()
    x_axis = np.array(wavelengths)
        
    total_spectrum = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    H2O = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    CO2 = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    ice_cloud = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    liquid_cloud = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    rayleigh = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    collisions = pd.DataFrame(index=number_of_rows, columns=number_of_columns)

    for file_number in range(0,len(files)):
        data = open(files[file_number], 'r')
        lines = data.readlines()
        lines = lines[1129:1328]
        data.close()

        for row in range(0,198):
            list_of_datapoints = lines[row].split('  ')
            total_spectrum.loc[row, file_number] = float(list_of_datapoints[1])
            H2O.loc[row, file_number] = float(list_of_datapoints[3])
            CO2.loc[row, file_number] = float(list_of_datapoints[4])
            ice_cloud.loc[row, file_number] = float(list_of_datapoints[5])
            liquid_cloud.loc[row, file_number] = float(list_of_datapoints[6])
            rayleigh.loc[row, file_number] = float(list_of_datapoints[7])
            collisions.loc[row, file_number] = float(list_of_datapoints[8])

    meaned_total_spectrum = 100*(1-total_spectrum.mean(axis=1).to_numpy())
    meaned_H2O = 100*(1-H2O.mean(axis=1).to_numpy())
    meaned_CO2 = 100*(1-CO2.mean(axis=1).to_numpy())
    meaned_ice_cloud = 100*(1-ice_cloud.mean(axis=1).to_numpy())
    meaned_liquid_cloud = 100*(1-liquid_cloud.mean(axis=1).to_numpy())
    meaned_rayleigh = 100*(1-rayleigh.mean(axis=1).to_numpy())
    meaned_collisions = 100*(1-collisions.mean(axis=1).to_numpy())
       
    # transit_depth = (7.16e06*meaned_total_spectrum)/(10*6.8e03)    
    
    # plt.plot(x_axis, transit_depth)
    # plt.title('Transit depth')
    # plt.xlabel('Wavelength [um]')
    # plt.ylabel('Depth')
    # plt.show()
    
    plt.plot(x_axis, meaned_total_spectrum)
    plt.title('Absorption spectrum')
    plt.xlabel('Wavelength [um]')
    plt.ylabel('Absorption [%]')
    plt.ylim([0,100])
    plt.show()
    
    plt.plot(x_axis, meaned_total_spectrum, linestyle='-', color='r', label='Total')
    plt.plot(x_axis, meaned_H2O, linestyle='-', color='b', label='Vapour')
    plt.plot(x_axis, meaned_ice_cloud, linestyle='-', color='k', label='Ice cloud')
    plt.plot(x_axis, meaned_liquid_cloud, linestyle='--', color='k', label='Liquid cloud')
    plt.title('Breakdown of water only')
    plt.xlabel('Wavelength [um]')
    plt.ylabel('Absorption [%]')
    plt.ylim([0,100])
    plt.legend()
    plt.show()
    
    plt.plot(x_axis, meaned_total_spectrum, linestyle='-', color='r', label='Total')
    plt.plot(x_axis, meaned_H2O, linestyle='-', color='g', label='Vapour')
    plt.plot(x_axis, meaned_CO2, linestyle='--', color = 'b', label='CO2')
    plt.plot(x_axis, meaned_ice_cloud, linestyle='-', color='k', label='Ice cloud')
    plt.plot(x_axis, meaned_liquid_cloud, linestyle='--', color='k', label='Liquid cloud')
    plt.plot(x_axis, meaned_rayleigh, linestyle=':', color='k', label='Rayleigh scattering')
    plt.plot(x_axis, meaned_collisions, linestyle='-.', color='k', label='Collision-induced absorption')
    plt.title('Breakdown of absorption spectrum')
    plt.xlabel('Wavelength [um]')
    plt.ylabel('Absorption [%]')
    plt.ylim([0,100])
    plt.legend(loc='upper left', fontsize='x-small')
    plt.show()


def plot_transitdepth(path, day=0):             
            
    files = glob.glob(str(path) + 'spectra/*.txt')    
    
    number_of_columns = []
    for number in range(len(files)):
        number_of_columns.append(number)
    number_of_rows = []
    for number in range(198):
        number_of_rows.append(number)
    
    wavelengths = []
    first_file = open(files[0], 'r')
    rad_spectrum = first_file.readlines()
    rad_spectrum = rad_spectrum[658:856]
    for item in rad_spectrum:
        datapoints = item.split('  ')
        wavelength = float(datapoints[0])
        wavelengths.append(wavelength)
    first_file.close()
    x_axis = np.array(wavelengths)
    
    total_spectrum = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    noise = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    stellar = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    planet = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    transit = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    blocked = pd.DataFrame(index=number_of_rows, columns=number_of_columns)
    
    for file_number in range(0,len(files)):
        data = open(files[file_number], 'r')
        lines = data.readlines()
        lines = lines[658:856]
        data.close()

        for row in range(0,198):
            lines[row] = lines[row].replace(' -', '  ')
            list_of_datapoints = lines[row].split('  ')
            total_spectrum.loc[row, file_number] = float(list_of_datapoints[1])
            noise.loc[row, file_number] = float(list_of_datapoints[2])
            stellar.loc[row, file_number] = float(list_of_datapoints[3])
            planet.loc[row, file_number] = float(list_of_datapoints[4])
            transit.loc[row, file_number] = float(list_of_datapoints[5])
            blocked.loc[row, file_number] = float(list_of_datapoints[6])

    meaned_total_spectrum = total_spectrum.mean(axis=1).to_numpy()
    meaned_noise = noise.mean(axis=1).to_numpy()
    meaned_stellar = stellar.mean(axis=1).to_numpy()
    meaned_planet = planet.mean(axis=1).to_numpy()
    meaned_transit = transit.mean(axis=1).to_numpy()
    meaned_blocked = blocked.mean(axis=1).to_numpy()
    continuum = np.min(meaned_transit)
    
    with open(str(path) + 'output/transit_day%s.txt' %(day), 'w') as file:
        file.write(str(x_axis) + '\n')
        file.write(str(meaned_transit) + '\n')                              
    file.close()
    
    plt.plot(x_axis, (meaned_transit-continuum)*1e6)
    plt.title('Relative transit depth, day=%s' %(day+1))
    plt.xlabel('Wavelength [um]')
    plt.ylabel('Relative transit depth [ppm]')
    plt.annotate('H20', xy=(1.9507,8), xytext=(0, 3), textcoords='offset points')
    plt.annotate('H20', xy=(1.4330,3), xytext=(0, 3), textcoords='offset points')
    plt.annotate('H20', xy=(2.6293,4), xytext=(0, 2), textcoords='offset points')
    plt.annotate('CO2', xy=(4.3250,20), xytext=(8, 2), textcoords='offset points')
    plt.annotate('CO2', xy=(2.0099,15), xytext=(1, 1), textcoords='offset points')
    plt.annotate('CO2', xy=(2.7089,20), xytext=(8, 2), textcoords='offset points')
#    plt.xlim(1,5)
#    plt.ylabel('$(R_p/R_{star})^2$')
#    plt.ylim([0,1])
    plt.show()
 
