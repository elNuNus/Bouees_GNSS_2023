"""
Build directories used to store data logged by the buoy.

@author: Baptiste Menetrier
"""

import os

root = '/home/pi/data'
os.system(f"mkdir {root}")

listFolder = ['NMEA', 'UBX', 'METEO', 'RINEX']

for folder in listFolder:
    os.system(f"mkdir {root}/{folder}")
