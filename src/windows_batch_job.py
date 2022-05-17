#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 21:17:40 2022

@author: Mo Cohen
"""
import subprocess
import glob
from pathlib import Path

first=300
last=350
parentpath = 'R:/psg_files/trapcontrol'


def psg(daypath, day=-1):

    """ Send previously made configuration files to local version of PSG """
        
    for latitude in range(0,90):
        east_filename = str(daypath) + 'configfiles/config_%s_36.txt' %(latitude)
        east_cmd = 'curl -d type=all -d whdr=y --data-urlencode file@%s http://localhost:3000/api.php' %(east_filename)
        with open(str(daypath) + 'spectra/trn_%s_36.txt' %(latitude), 'w') as file:
            subprocess.run(east_cmd, shell=True, stdout=file)
        file.close()
        
        west_filename = str(daypath) + 'configfiles/config_%s_108.txt' %(latitude)
        west_cmd = 'curl -d type=all -d whdr=y --data-urlencode file@%s http://localhost:3000/api.php' %(west_filename)
        with open(str(daypath) + 'spectra/trn_%s_108.txt' %(latitude), 'w') as file:
            subprocess.run(west_cmd, shell=True, stdout=file)
        file.close()
        print('Up to latitude: ' + str(latitude))

    
for day in range(first,last+1):
    daypath = str(parentpath) + 'trap_day%s/' %(day)
    Path(str(daypath)).mkdir(exist_ok=True)
    psg(daypath, day=day)