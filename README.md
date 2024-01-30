# GNSS Buoy (School project)

## Description
This is our 2nd year engineering school project, directed by @pbosser.

Our goal is to make a low-cost GNSS buoy system for various weather measurements.
>(The original project was written and documented in French, and we chose to write everything in English so that anyone can replicate our project.)

This project is a "reboot" of a previous 3rd year project (hence the fork from https://github.com/Zackary-Vanche/Bouees_GNSS). We made a couple modifications, described below.
- __remote access to acquired data__ : the buoy system will send via cellular network its acquired data to a remote server, which will then be accessible for any user.
- __a WiFi remote switch__ : we want any user to remotely access a buoy without the need of a wired connection. The Raspberry will act as a WiFi access point which the user can connect to. We will use a Bluetooth connection to trigger the Access Point activation.



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
