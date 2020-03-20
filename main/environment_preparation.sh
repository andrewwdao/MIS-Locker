#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi

echo
echo "CAUTION: "
echo "This script will turn this operating system into a read-only one and turn off bluetooth completely."
echo "Then, it will install the must-have pre-requisites and prepare the environment for MISlocker system."
echo "Back up should be made where needed before proceed."
echo "Recommended to install on a fresh Raspbian Buster."
echo -n "Confirm to install? [Y/N]"

read input

if ! [ $input == "y" ] || [ $input == "Y" ]; then
	{ echo "Exiting..."; exit 1; }
fi

echo "Installing..."

# automatically get and set time from the internet (workaround for proxy setting)
date -s "$(wget -qSO- --max-redirect=0 google.vn 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

apt-get update && apt-get upgrade -y

# pip installation
apt-get install python3-pip -y

# git installation
apt-get install wget git -y

# fingerprint package install  ## https://sicherheitskritisch.de/2015/03/fingerprint-sensor-fuer-den-raspberry-pi-und-debian-linux-en/
# using modified version - local version with newest packages
pip3 install pyxdg==0.26
pip3 install urllib3==1.25.6
pip3 install Pillow # this one will install the latest Pillow
#	sudo apt-get install python3-pil -y # this one will not install the latest Pillow
apt-get install libopenjp2-7 # reference: https://github.com/rm-hull/luma.led_matrix/issues/154
apt-get install libtiff5 -y


# Pyserial package install  ## https://pyserial.readthedocs.io/en/latest/shortintro.html#opening-serial-ports
apt-get install python3-serial -y
if [ 0 -eq $( grep -c 'enable_uart = 1' /boot/config.txt ) ]; then # check if the phrase "enable_uart = 1" existed in the file or not
	echo "enable_uart = 1" | tee -a /boot/config.txt
fi
										## https://pypi.org/project/smbus2/
# I2C package install - smbus - smbus2  ## https://raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
if [ 0 -eq $( grep -c 'i2c-dev' /etc/modules ) ]; then # check if the phrase "i2c-dev" existed in the file or not
	echo "i2c-dev" | tee -a /etc/modules
fi
if [ 0 -eq $( grep -c 'i2c-bcm2708' /etc/modules ) ]; then # check if the phrase existed in the file or not
	echo "i2c-bcm2708" | tee -a /etc/modules
fi
apt-get install -y python-smbus python3-smbus i2c-tools
pip3 install smbus2

# RPi.GPIO
pip3 install RPi.GPIO

# WiringPi  ## http://wiringpi.com/
apt-get install wiringpi -y

#Flask - WTForm - SQLAlchemy - Migrate - Bootstrap  ## https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
pip3 install flask
pip3 install python-dotenv
pip3 install flask-wtf
pip3 install flask-sqlalchemy
pip3 install flask-migrate
pip3 install flask-bootstrap

# update all the kept-back if existed  # # https://askubuntu.com/questions/601/the-following-packages-have-been-kept-back-why-and-how-do-i-solve-it
apt-get --with-new-pkgs upgrade -y

cd /home/$(who am i | awk '{print $1}')/ # return to home folder -- cannot use $USER or $LOGNAME since they may return root. $SUDO_USER can also be used but not all covered. ref: https://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands

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
cd ./main #./system/main
make clean
rm -rf ./obj
mkdir ./obj
make rfid_main peripheral_init peripheral_main buzzer_main

# provide priveledge for environment preparation itself
chmod +x environment_preparation.sh
chmod +x update_time_proxy_readonly.sh
chmod +x bluetooth_deactivate.sh

# activate system on start-up
cp MIStime.service /etc/systemd/system
systemctl enable MIStime.service
cp MISinit.service /etc/systemd/system
systemctl enable MISinit.service
cp MISlocker.service /etc/systemd/system
systemctl enable MISlocker.service

# check if the file exist outside or not, if yes --> cleanup
cd /home/$(who am i | awk '{print $1}')/ # return to home folder -- cannot use $USER or $LOGNAME since they may return root. $SUDO_USER can also be used but not all covered. ref: https://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands
if [ -f "./environment_preparation.sh" ] ; then
	rm -rf environment_preparation.sh
fi

# disable bluetooth
{./bluetooth_deactivate.sh}

# make system read-only

echo 
echo 
echo "Done. Please restart to the changes take effect!"

# (c) 2020 Minh-An Dao, Can Tho University