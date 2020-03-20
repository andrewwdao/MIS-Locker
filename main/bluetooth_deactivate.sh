#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi


#echo "This program will deactivate bluetooth on this Raspberry Pi device."
#echo -n "Confirm to install? [Y/N]"

#read input

#if ! [ $input == "y" ] || [ $input == "Y" ]; then
#	{ echo "Exiting..."; exit 1; }
#fi

echo "Deactivating bluetooth..."

# Bluetooth disable and remove
echo "dtoverlay=pi3-disable-bt" | tee -a /boot/config.txt # Disable Bluetooth boot
systemctl disable hciuart.service # Disable systemd service that initializes Bluetooth Modems connected by UART
#systemctl disable bluealsa.service
systemctl disable bluetooth.service
systemctl disable bluetooth cron 
apt-get remove -y bluez
apt-get autoremove -y

# ref: https://scribles.net/disabling-bluetooth-on-raspberry-pi/

# (c) 2020 Minh-An Dao, Can Tho University