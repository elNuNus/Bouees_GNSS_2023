#!/bin/bash
echo "$(date): Starting hourly tasks" >> /var/log/cron_task.log
# Manually shutdown gpsd to stop writing to log files
echo "$(date): Hourly task - Shutdown gpsd process" >> /var/log/cron_task.log
/home/pi/BuoyConfig/shutdown_gpsd.sh
# Rotate log files
echo "$(date): Hourly task - Rotate log files" >> /var/log/cron_task.log
/usr/sbin/logrotate /home/pi/BuoyConfig/logrotate.conf --state /home/pi/BuoyConfig/logrotate-state
# Manually restart gpsd
echo "$(date): Hourly task - Restart gpsd process" >> /var/log/cron_task.log
/home/pi/BuoyConfig/startup_gpsd.sh
# Restart writing to log files
echo "$(date): Hourly task - Start logging UBX data" >> /var/log/cron_task.log
gpspipe -o /home/pi/data/UBX/logUBX.ubx -R -l

#@hourly gpspipe -o /home/pi/data/NMEA/logNMEA.txt -r -l
