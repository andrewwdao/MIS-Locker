#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi

echo
echo "CAUTION: must be placed with the C files and Makefile"
echo
echo "Renewing binary files ... "
echo

# go to main code section, clean the c binary files and re-create them
make clean   # cd /home/$(who am i | awk '{print $1}')/system/main
rm -rf ./obj
mkdir ./obj
make rfid_main peripheral_init peripheral_main buzzer_main

# provide priveledge for setup itself
chmod +x ../setup.sh
chmod +x time_updater_proxy_readonly.sh
chmod +x bluetooth_disable.sh
chmod +x ./readonly/setup.sh

echo 
echo "Done."

# (c) 2020 Minh-An Dao, Can Tho University