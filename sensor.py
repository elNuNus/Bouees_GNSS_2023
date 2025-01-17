import bme280
import smbus2
from datetime import datetime
from time import sleep


# Load settings:
setting_file = '/home/pi/ScriptPython/capteur_settings.txt'
with open(setting_file, 'r') as f:
    line = f.readline()
    settings = line.split(',')
    #print(settings)
    
save_temperature = bool(int(settings[0]))
save_pressure = bool(int(settings[1]))
save_humidity = bool(int(settings[2]))
Ts = int(settings[3]) # Sampling period

port = 1
address = 0x77 # Adafruit BME280 address. Other BME280s may be different
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)


# ~ file = '/home/pi/data/METEO/logMETEO.txt'
# Write header 
# ~ with open(file, 'w') as f:
    # ~ header = 'date,'
    # ~ if save_temperature:
        # ~ header += ' temperature_C,'
    # ~ if save_pressure:
        # ~ header += ' pression_hPa,'
    # ~ if save_humidity:
        # ~ header += ' humidity_per,'
    # ~ header = header[:-1] # remove last comma 
    # ~ header += '\n' 
    # ~ f.write(header)

while True:
    # Get sensor data
    bme280_data = bme280.sample(bus, address)

    # Get current date
    now = datetime.now()
    date = now.strftime("%d%m%Y %H:%M:%S")


    line = f'{date},'
    if save_temperature:
        line += f'{bme280_data.temperature},'
    if save_pressure:
        line += f'{bme280_data.pressure},'
    if save_humidity:
        line += f'{bme280_data.humidity},'
        
    line = line[:-1] # remove last comma 
    line += '\n' 
    print(line)
    # Write log
    # ~ with open(file, 'a') as f:
        # ~ f.write(line)

    # ~ sleep(Ts)


