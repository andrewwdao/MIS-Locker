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
echo "Recommended to install on a fresh Raspbian Buster."
echo
echo "Make sure wifi is connected."
echo "Back up should be made where needed before proceed."
echo
echo -n "Confirm to install? [Y/N]"

read input

if ! [ $input == "y" ] || [ $input == "Y" ]; then
	{ echo "Exiting..."; exit 1; }
fi

echo "Installing..."

# automatically get and set time from the internet (workaround for proxy setting)
date -s "$(wget -qSO- --max-redirect=0 google.vn 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

apt-get update
apt-get upgrade -y

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

# Flask - WTForm - SQLAlchemy - Migrate - Bootstrap  ## https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
pip3 install flask
pip3 install python-dotenv
pip3 install flask-wtf
pip3 install flask-sqlalchemy
pip3 install flask-migrate
pip3 install flask-bootstrap
# Gevent networking platform to deploy production server - https://pypi.org/project/gevent/#downloads
pip3 install gevent

# update all the kept-back if existed  # # https://askubuntu.com/questions/601/the-following-packages-have-been-kept-back-why-and-how-do-i-solve-it
apt-get --with-new-pkgs upgrade -y

cd /home/$(who am i | awk '{print $1}')/ # return to home folder -- cannot use $USER or $LOGNAME since they may return root. $SUDO_USER can also be used but not all covered. ref: https://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands

# download system files from git repository
if [ -d "./system" ] ; then  # check if the directory exist or not
	rm -rf ./system
fi
git clone https://github.com/minhan74/MIS-Locker.git
# change name
mv MIS-Locker/ system/

# go to main code section, clean the c binary files and re-create them
# and provide priveledge for setup itself
cd /home/$(who am i | awk '{print $1}')/system/main # /home/<user>/system/main
chmod +x binary_renewer.sh
./binary_renewer.sh

# setup server database for admin login
chmod +x server-db_setup.sh
./server-db_setup.sh

# --- activate system on start-up

# MISinit.service
echo "[Unit]
Description=MISlocker peripheral initialization service
DefaultDependencies=false
Requires=systemd-modules-load.service
After=systemd-modules-load.service
Before=sysinit.target
ConditionPathExists=/sys/class/i2c-adapter

[Service]
Type=oneshot
ExecStart=sudo python3 -u sysinit.py
WorkingDirectory=/home/$(who am i | awk '{print $1}')/system/main
Restart=no
# must set user to root to execute all functions and peripherals
User=root

[Install]
WantedBy=sysinit.target

# reference: https://www.raspberrypi.org/forums/viewtopic.php?t=221507
" > /etc/systemd/system/MISinit.service # append multiple lines to a file : https://unix.stackexchange.com/questions/77277/how-to-append-multiple-lines-to-a-file

# MIStime.service
#echo "[Unit]
#Description=Time set up workaround service for MISlocker
#Requires=network-online.target
#After=multi-user.target
#DefaultDependencies=true
#
#[Service]
#Type=oneshot
#ExecStart=/home/$(who am i | awk '{print $1}')/system/main/time_updater_proxy_readonly.sh
#Restart=no
## must set user to root to execute all functions and peripherals
#User=root
#
#[Install]
#WantedBy=sysinit.target multi-user.target
#" > /etc/systemd/system/MIStime.service # append multiple lines to a file : https://unix.stackexchange.com/questions/77277/how-to-append-multiple-lines-to-a-file

# MISlocker.service
echo "[Unit]
Description=MISlocker main service
After=multi-user.target
DefaultDependencies=true

[Service]
Type=simple
# This will release the same result: ExecStart = /usr/bin/sudo python3 -u main.py
ExecStart=sudo python3 -u main.py
WorkingDirectory=/home/$(who am i | awk '{print $1}')/system/main
StandardOutput=inherit
StandardError=inherit
Restart=yes
# must set user to root to execute all functions and peripherals
User=root
# SIGINT is translated as a KeyboardInterrupt exception by Python.
# default kill signal is SIGTERM which doesn't raise an exception in Python.
# KillSignal=SIGINT
# Additional commands that are executed after the service is stopped. ref: https://www.freedesktop.org/software/systemd/man/systemd.service.html
ExecStopPost=sudo python3 -u syshalt.py

[Install]
WantedBy=sysinit.target multi-user.target
" > /etc/systemd/system/MISlocker.service # append multiple lines to a file : https://unix.stackexchange.com/questions/77277/how-to-append-multiple-lines-to-a-file

# old method, wont work for any user
# cp MISinit.service /etc/systemd/system
# cp MIStime.service /etc/systemd/system
# cp MISlocker.service /etc/systemd/system

systemctl enable MISinit.service
# systemctl enable MIStime.service
systemctl enable MISlocker.service

# check if the file exist outside or not, if yes --> cleanup
cd /home/$(who am i | awk '{print $1}')/ # return to home folder -- cannot use $USER or $LOGNAME since they may return root. $SUDO_USER can also be used but not all covered. ref: https://stackoverflow.com/questions/4598001/how-do-you-find-the-original-user-through-multiple-sudo-and-su-commands
if [ -f "./setup.sh" ] ; then
	rm -rf setup.sh
fi

# disable bluetooth
/home/$(who am i | awk '{print $1}')/system/main/bluetooth_disable.sh

# make system read-only
cd /home/$(who am i | awk '{print $1}')/system/main/readonly
./setup.sh yes

echo 
echo 
echo "Done. Please restart for the changes take effect!"

# (c) 2020 Minh-An Dao, Can Tho University