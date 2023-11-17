#!/bin/bash
# Boot task to start recording GNSS data with dedicated cron task
LOG_FILE=/var/log/cron_task.log
RECORD_UBX=1

# Start recording UBX data
if [ $RECORD_UBX -eq 1 ]
then
	#echo "test"
	echo "$(date): Start UBX recording" >> $LOG_FILE
	gpspipe -o /home/pi/data/UBX/logUBX.ubx -R >> $LOG_FILE
fi
