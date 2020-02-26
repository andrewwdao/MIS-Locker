#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

echo This program will install the must-have pre-requisites for MISlocker system
echo You must install pip3 and git before proceed. Confirm? [Y/N]

read input

if [ $input == "y" ] || [ $input == "Y" ]; then
	echo Installing...

	sudo apt-get update && sudo apt-get upgrade

	# fingerprint package install  ## https://sicherheitskritisch.de/2015/03/fingerprint-sensor-fuer-den-raspberry-pi-und-debian-linux-en/
	if [ ! grep -Fxq "deb http://apt.pm-codeworks.de wheezy main" /etc/apt/sources.list]; then
		echo "deb http://apt.pm-codeworks.de wheezy main" | sudo tee -a /etc/apt/sources.list
		wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | sudo apt-key add -
	fi
	sleep 0.5
	sudo apt-get install python3-fingerprint -y
	sudo usermod -a -G dialout MISlocker
	
	# Pyserial package install  ## https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports
	sudo apt-get install python3-serial -y
	if [ ! grep -Fxq "enable_uart = 1" /boot/config.txt]; then
		echo "enable_uart = 1" | sudo tee -a /boot/config.txt
	fi
	
											## https://pypi.org/project/smbus2/
	# I2C package install - smbus - smbus2  ## https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
	if [ ! grep -Fxq "i2c-dev" /etc/modules]; then
		echo "i2c-dev" | sudo tee -a /etc/modules
	fi
	if [ ! grep -Fxq "i2c-bcm2708" /etc/modules]; then
		echo "i2c-bcm2708" | sudo tee -a /etc/modules
	fi
	sudo apt-get install -y python-smbus python3-smbus i2c-tools
	pip3 install smbus2
	
	# RPi.GPIO
	pip3 install RPi.GPIO
	
	# WiringPi  ## http://wiringpi.com/
	sudo apt-get install wiringpi -y
	
	#Flask - WTForm - SQLAlchemy - Migrate - Bootstrap  ## https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
	pip3 install flask
	pip3 install python-dotenv
	pip3 install flask-wtf
	pip3 install flask-sqlalchemy
	pip3 install flask-migrate
	pip3 install flask-bootstrap
	
	# clean the c binary files and re-create them
	make clean
	rm -rf ./obj
	mkdir ./obj
	make rfid_main peripheral_init peripheral_main buzzer_main
	
	
	echo 
	echo 
	echo Done. Please restart to the changes take effect!
fi

# (c) 2020 Minh-An Dao, Can Tho University