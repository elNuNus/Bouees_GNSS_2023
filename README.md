# GNSS Buoy (School project)

## Description

## Software
This repository contains all the files necessary to deploy our system on a Raspberry Pi (preferably Zero W or Zero 2).

__--Please code and comment your code in ENGLISH.--__

The files are organised as follows :
  - do_log.py : program used for logging and recording data from the sensors. It uses as input the sensor configurations indicated in the log.conf file.
  - log.conf : configuration file for logging raw data (read in do_log.py).
  - gnsstime.py : python library for date and time management.

## Hardware
The hardware we used for this project is the following :

  - 1 (or more) Raspberry Pi Zero 2, used to act as the entry point of our system
  - 1 (or more) Ublox Ardusimple chip, used with an antenna for GNSS signal acquisiton
  - 1 Intel NUC, used to host the server on wich any user can access the data from the Raspberry Pi

## Web Interface
Please see our Web Interface repository for additional information : [repository name]
