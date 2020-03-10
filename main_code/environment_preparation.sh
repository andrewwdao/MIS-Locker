#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

echo This program will install the must-have pre-requisites for MISlocker system
echo Confirm to install? [Y/N]

read input

if [ $input == "y" ] || [ $input == "Y" ]; then
	echo Installing...
	
	# automatically get and set time from the internet (workaround for proxy setting)
	sudo date -s "$(wget -qSO- --max-redirect=0 google.vn 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
	
	sudo apt-get update && sudo apt-get upgrade -y
	
	# pip installation
	sudo apt-get install python3-pip -y
	
	# git installation
	sudo apt-get install wget git -y
	
	# fingerprint package install  ## https://sicherheitskritisch.de/2015/03/fingerprint-sensor-fuer-den-raspberry-pi-und-debian-linux-en/
	if ! grep -Fxq "deb http://apt.pm-codeworks.de wheezy main" /etc/apt/sources.list ; then
		echo "deb http://apt.pm-codeworks.de wheezy main" | sudo tee -a /etc/apt/sources.list
		wget -O - http://apt.pm-codeworks.de/pm-codeworks.de.gpg | sudo apt-key add -
		sudo apt-get update && sudo apt-get upgrade -y #update catch again before install the package below
	fi
	
	sudo apt-get install python3-fingerprint -y
	sudo usermod -a -G dialout $USER
	
	# Pyserial package install  ## https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports
	sudo apt-get install python3-serial -y
	if ! grep -Fxq "enable_uart = 1" /boot/config.txt ; then
		echo "enable_uart = 1" | sudo tee -a /boot/config.txt
	fi
	
											## https://pypi.org/project/smbus2/
	# I2C package install - smbus - smbus2  ## https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
	if ! grep -Fxq "i2c-dev" /etc/modules ; then
		echo "i2c-dev" | sudo tee -a /etc/modules
	fi
	if ! grep -Fxq "i2c-bcm2708" /etc/modules ; then
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
	
	# download system files from git repository
	if [ -d "./system" ] ; then  # check if the directory exist or not
		rm -rf ./system
	fi
	mkdir ./system
	cd ./system
	git init
	git remote add origin https://github.com/minhan74/MIS-Locker.git
	git pull origin master
	
	
	# go to main code section, clean the c binary files and re-create them
	cd ./main_code #./system/main_code
	make clean
	rm -rf ./obj
	mkdir ./obj
	make rfid_main peripheral_init peripheral_main buzzer_main
	
	# activate system in start-up
	sudo cp sysinit.service /etc/systemd/system
	sudo systemctl enable sysinit.service
	
	echo 
	echo 
	echo Done. Please restart to the changes take effect!
fi

# (c) 2020 Minh-An Dao, Can Tho University