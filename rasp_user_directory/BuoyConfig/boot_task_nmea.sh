#!/bin/bash
# Boot task to start recording GNSS data with dedicated cron task
LOG_FILE=/var/log/cron_task.log
RECORD_NMEA=1

# Start recording NMEA data
if $RECORD_NMEA; then
	echo "$(date): Start NMEA recording" >> $LOG_FILE
	gpspipe -o /home/pi/data/NMEA/logNMEA.txt -r >> $LOG_FILE
fi
