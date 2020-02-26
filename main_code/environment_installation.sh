#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

echo You must install pip3 and git before proceed. Confirm? [Y/N]

read input

if [ $input == "y" ] || [ $input == "Y" ]; then
	echo Installing the must-have pre-requisites for MISlocker

	sudo apt-get update && sudo apt-get upgrade

	# fingerprint package install ## https://sicherheitskritisch.de/2015/03/fingerprint-sensor-fuer-den-raspberry-pi-und-debian-linux-en/
	echo "deb http://apt.pm-codeworks.de wheezy main" | sudo tee -a /etc/apt/sources.list
	wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | sudo apt-key add -
	sudo apt-get install python-fingerprint
	sudo usermod -a -G dialout MISlocker
	
	# Pyserial package install
	sudo apt-get install python3-serial
	echo "enable_uart = 1" | sudo tee -a /boot/config.txt
	
	# I2C package install - smbus - smbus2
	echo "i2c-dev" | sudo tee -a /etc/modules
	echo "i2c-bcm2708" | sudo tee -a /etc/modules
	sudo apt-get install -y python-smbus python3-smbus i2c-tools
	pip3 install smbus2
	
	# RPi.GPIO
	pip3 install RPi.GPIO
	
	# WiringPi
	sudo apt-get install wiringpi
	
	#Flask - WTForm - SQLAlchemy - Migrate - Bootstrap
	pip3 install flask
	pip3 install python-dotenv
	pip3 install flask-wtf
	pip3 install flask-sqlalchemy
	pip3 install flask-migrate
	pip3 install flask-bootstrap
	
	echo Done.
fi

# (c) 2020 Minh-An Dao, Can Tho University