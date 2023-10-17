# -*- coding: utf-8 -*-
"""

This script is used to do some acquisition, apparently. [more documentation needed]

@author: utilisateur?

"""

import os
import time
import shutil
from datetime import datetime

time.sleep(120) # Wait for synchronisation 


# Path definition
# root = r'C:\Users\33686\Desktop\ENSTAB\Cours\3A\Guerledan\testPy' # Test sous windows

root = r'.'

pathData = f'{root}/data'
# pathData = f'{root}\\data' # Test sous windows 

T_NMEA = 10 # Save NMEA every 10 min

# Remove former folder 'acquisition'
os.system(f'rm -r {pathData}')

# Create new folder 'acquisition'
os.system(f'mkdir {pathData}')


while True:
    now = datetime.now()
    current_min = now.minute
    current_sec = now.second

    pathfolderHour = f'{pathData}/{now.strftime("%d%m%Y_%H00")}' # access path to folder concatenated with date and hour
    # pathfolderHour = f'{pathData}\{now.strftime("%d%m%Y_%H00")}' # Test on windows

    if ~os.path.exists(pathfolderHour): # if folder does not exist
        os.system(f'mkdir {pathfolderHour}') # create folder

    filename = now.strftime("%d%m%Y_%H00")
    outputFilePath_RAW = f'{pathfolderHour}/{filename}_RAW.ubx' # access path to .ubx file (RAW data)
    outputFilePath_NMEA = f'{pathfolderHour}/{filename}_NMEA.txt' # access path to .txt file (NMEA data)

    # outputFilePath_RAW = f'{pathfolderHour}\{filename}_RAW.ubx' # Test on windows
    # outputFilePath_NMEA = f'{pathfolderHour}\{filename}_NMEA.txt' # Test on windows

    cmdRAW =  f'gpspipe -o {outputFilePath_RAW} -R' # command to save RAW data to the designated path
    cmdNMEA = f'gpspipe -o {outputFilePath_NMEA} -r' # command to save NMEA data to the designated path

    #TODO : find out where the data is coming from (which port)

    #--Save RAW
    os.system(cmdRAW)
    # os.system(f'echo.>{outputFilePath_RAW}')U
    # print(cmdRAW)

    #--Save NMEA
    if (current_min%T_NMEA == 0) & (current_sec == 0): # Save NMEA every T_NMEA minutes
        os.system(cmdNMEA)
        # os.system(f'echo.>{outputFilePath_NMEA}')
        # print(cmdNMEA)

    

 
