#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

sudo -n true
test $? -eq 0 || exit 1 "you should have sudo priveledge to run this script"

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root!"
  exit 1;
fi

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
	# using modified version - local version with newest packages
	sudo pip3 install pyxdg==0.26
	sudo pip3 install urllib3==1.25.6
	sudo pip3 install Pillow # this one will install the latest Pillow
	#	sudo apt-get install python3-pil -y # this one will not install the latest Pillow
	sudo apt-get install libopenjp2-7 # reference: https://github.com/rm-hull/luma.led_matrix/issues/154
	sudo apt-get install libtiff5 -y
	
	
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
	sudo pip3 install smbus2
	
	# RPi.GPIO
	sudo pip3 install RPi.GPIO
	
	# WiringPi  ## http://wiringpi.com/
	sudo apt-get install wiringpi -y
	
	#Flask - WTForm - SQLAlchemy - Migrate - Bootstrap  ## https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
	sudo pip3 install flask
	sudo pip3 install python-dotenv
	sudo pip3 install flask-wtf
	sudo pip3 install flask-sqlalchemy
	sudo pip3 install flask-migrate
	sudo pip3 install flask-bootstrap
	
	# update all the kept-back if existed  # # https://askubuntu.com/questions/601/the-following-packages-have-been-kept-back-why-and-how-do-i-solve-it
	sudo apt-get --with-new-pkgs upgrade -y
	
	cd /home/$(who am i | awk '{print $1}')/ # return to home folder -- cannot use $USER or $LOGNAME since they may return root. $SUDO_USER can also be used but not all covered. ref: https://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands
	
	# download system files from git repository
	if [ -d "./system" ] ; then  # check if the directory exist or not
		sudo rm -rf ./system
	fi
	sudo mkdir ./system
	cd ./system
	sudo git init
	sudo git remote add origin https://github.com/minhan74/MIS-Locker.git
	sudo git pull origin master
	
	
	# go to main code section, clean the c binary files and re-create them
	cd ./main #./system/main
	sudo make clean
	sudo rm -rf ./obj
	sudo mkdir ./obj
	sudo make rfid_main peripheral_init peripheral_main buzzer_main
	
	# provide priveledge for environment preparation itself
	sudo chmod +x environment_preparation.sh
	
	# activate system on start-up
	sudo cp MISinit.service /etc/systemd/system
	sudo systemctl enable MISinit.service
	sudo cp MISlocker.service /etc/systemd/system
	sudo systemctl enable MISlocker.service
	
	# check if the file exist outside or not, if yes --> cleanup
	cd /home/$(who am i | awk '{print $1}')/ # return to home folder -- cannot use $USER or $LOGNAME since they may return root. $SUDO_USER can also be used but not all covered. ref: https://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands
	if [ -f "./environment_preparation.sh" ] ; then
		sudo rm -rf environment_preparation.sh
	fi
	
	echo 
	echo 
	echo Done. Please restart to the changes take effect!
fi

# Bluetooth disable and remove
echo "dtoverlay=pi3-disable-bt" | tee -a /boot/config.txt # Disable Bluetooth boot
systemctl disable hciuart.service # Disable systemd service that initializes Bluetooth Modems connected by UART
systemctl disable bluealsa.service
systemctl disable bluetooth.service
systemctl disable bluetooth cron 
apt-get remove -y bluez
apt-get autoremove -y

# (c) 2020 Minh-An Dao, Can Tho University