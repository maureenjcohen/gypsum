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
last=301
parentpath = r'R:/psg_files/trapcontrol/'


def psg(parentpath, day=-1):

    """ Send previously made configuration files to local version of PSG """
                
	filename = str(parentpath) + 'configfiles/day_%s.txt' %(day)
	psg_cmd = 'curl -d type=all -d whdr=y --data-urlencode file@%s http://localhost:3000/api.php' %(filename)
	with open(str(parentpath) + 'spectra/trn_day_%s.txt' %(day), 'w') as file:
		subprocess.run(psg_cmd, shell=True, stdout=file)
	file.close()
	print('Up to day: ' + str(day))

    
for day in range(first,last+1):
    specpath = str(parentpath) + r'spectra/'
    Path(str(specpath)).mkdir(exist_ok=True)
    psg(parentpath, day=day)