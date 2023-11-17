#!/bin/bash
sudo systemctl start gpsd.socket
sudo systemctl start gpsd.service
sudo systemctl start gpsdctl@ttyACM0.service
