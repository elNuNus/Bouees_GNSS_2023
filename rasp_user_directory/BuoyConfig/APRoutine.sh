#!/bin/bash
LISTENING_TIME=120 # Time to wait for connection
CHECKING_CONNECTION_TIME=10
#LOGFILE=/var/log/cron_task.log
LOGFILE=/home/pi/log/cron_AP.log
sudo rfkill unblock wlan # Turn on AP
echo "$(date): Access Point turned ON" >> $LOGFILE

# Wait for connection
echo "$(date): Buoy waiting for connection.." >> $LOGFILE
sleep $LISTENING_TIME

# Check if any devices is connected to the AP
CONNECTED_DEVICES=$(sudo iw dev ap0 station dump)

if [ -z "$CONNECTED_DEVICES" ]; then
	echo "$(date): No devices connected to buoy" >> $LOGFILE
	sudo rfkill block wifi # Turn off AP
	echo "$(date): Access Point turned OFF" >> $LOGFILE
else
	CONNECTED_DEVICES=$(sudo iw dev ap0 station dump)
	while ! [ -z "$CONNECTED_DEVICES" ]
	do
		sleep $CHECKING_CONNECTION_TIME
		CONNECTED_DEVICES=$(sudo iw dev ap0 station dump)
		echo "$(date): Devices connected to buoy" >> $LOGFILE
	done
	echo "$(date): Devices disconnected from buoy" >> $LOGFILE
	sudo rfkill block wifi # Turn off AP
	echo "$(date): Access Point turned OFF" >> $LOGFILE
fi

