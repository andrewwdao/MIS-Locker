#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root!"
  exit 1;
fi


echo This script will turn this operating system into a read-only one.
echo Designed for MISlocker.
echo Confirm to install? [Y/N]

read input

if ! [ $input == "y" ] || [ $input == "Y" ]; then
	{ echo "Exiting..."; exit 1; }
fi

echo Installing...
	
# automatically get and set time from the internet (workaround for proxy setting)
sudo date -s "$(wget -qSO- --max-redirect=0 google.vn 2>&1 | grep Date: | cut -d' ' -f5-8)Z"
	
sudo apt-get update && sudo apt-get upgrade -y

echo "*** Installing some needed software..."
sudo apt-get install -y busybox-syslogd # ntp # watchdog
sudo apt-get install lsof -y

echo "***Removing some unneeded software..."
sudo systemctl disable dphys-swapfile.service
sudo systemctl disable apt-daily.service apt-daily.timer apt-daily-upgrade.timer apt-daily-upgrade.service
sudo systemctl disable logrotate.service logrotate.timer
sudo systemctl disable bootlogs
sudo systemctl disable console-setup
sudo apt-get remove --purge wolfram-engine triggerhappy anacron logrotate dphys-swapfile xserver-common lightdm rsyslog
sudo apt-get autoremove --purge -y
sudo dpkg --purge rsyslog

echo "*** Changing boot up parameters..."
# systemd-hostnamed uses a private temp folder on the root fs by default
# let's rather use /tmp
sudo sed -i.bck 's/PrivateTmp=yes/PrivateTmp=no/' /lib/systemd/system/systemd-hostnamed.service

if ! grep -Fxq "fastboot noswap ro" /boot/cmdline.txt ; then
	echo "*** Disable swap and filesystem check and set it to read-only..."
	sudo sed -i.bck '$s/$/ fastboot noswap ro/' /boot/cmdline.txt
fi


echo "*** Move some system files to temp filesystem..."
sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/run /var/spool /var/lock
sudo ln -s /tmp /var/lib/dhcp
sudo ln -s /tmp /var/lib/dhcpcd5
sudo ln -s /tmp /var/run
sudo ln -s /tmp /var/spool
sudo ln -s /tmp /var/lock

echo "*** Move resolv.conf to tmpfs..."
sudo mv /etc/resolv.conf /tmp/dhcpcd.resolv.conf
sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf

echo "*** Moving pids and other files to tmpfs..."
sudo sed -i.bck 's/PIDFile=\/run\/dhcpcd.pid/PIDFile=\/var\/run\/dhcpcd.pid/' /etc/systemd/system/dhcpcd5.service

sudo rm /var/lib/systemd/random-seed
sudo ln -s /tmp/random-seed /var/lib/systemd/random-seed

if ! grep -Fxq "ExecStartPre=" /lib/systemd/system/systemd-random-seed.service ; then
	sudo sed -i.bck '/RemainAfterExit=yes/a ExecStartPre=\/bin\/echo "" >\/tmp\/random-seed' /lib/systemd/system/systemd-random-seed.service   # append new line after a pattern. ref: https://unix.stackexchange.com/questions/121161/how-to-insert-text-after-a-certain-string-in-a-file
fi
	
sudo systemctl daemon-reload

if ! grep -Fxq "mount -o remount,rw" /etc/cron.hourly/fake-hwclock ; then
	sudo sed -i.bck '/fake\-hwclock save/i \ \ mount \-o remount,rw \/' /etc/cron.hourly/fake-hwclock   # append new line before a pattern. ref: https://unix.stackexchange.com/questions/121161/how-to-insert-text-after-a-certain-string-in-a-file
	sudo sed -i.bck '/fake\-hwclock save/a \ \ mount \-o remount,ro \/' /etc/cron.hourly/fake-hwclock   # append new line after a pattern. ref: https://unix.stackexchange.com/questions/121161/how-to-insert-text-after-a-certain-string-in-a-file
fi

# sudo sed -i.bak '/driftfile/c\driftfile /tmp\/ntp.drift' /etc/ntp.conf

# echo "* Setting up tmpfs for lightdm, in case this isn't a headless system."
# sudo ln -fs /tmp/.Xauthority /home/pi/.Xauthority
# sudo ln -fs /tmp/.xsession-errors /home/pi/.xsession-errors

echo "*** Setting fs as ro in fstab..."
if [ 0 -eq $( grep -c ',ro' /etc/fstab ) ]; then
	sudo sed -i 's/\bvfat    defaults\b/&,ro/' /etc/fstab   # append words into existing line. ref: https://stackoverflow.com/questions/35252285/insert-text-with-sed-on-the-same-line-that-pattern-search
	sudo sed -i 's/\bext4    defaults\b/&,ro/' /etc/fstab   # append words into existing line. ref: https://stackoverflow.com/questions/35252285/insert-text-with-sed-on-the-same-line-that-pattern-search
	
	sudo tee -a /etc/fstab > /dev/null <<CONTENT1
tmpfs           /tmp             tmpfs   nosuid,nodev         0       0
tmpfs           /var/log         tmpfs   nosuid,nodev         0       0
tmpfs           /var/tmp         tmpfs   nosuid,nodev         0       0
tmpfs           /var/lib/dhcpcd5 tmpfs   nosuid,nodev         0       0
tmpfs           /var/lib/sudo/ts tmpfs   nosuid,nodev         0       0
CONTENT1

fi

echo "*** Modifying bashrc..."
if [ 0 -eq $( grep -c 'mount -o remount' /etc/bash.bashrc ) ]; then
	# BE CAREFUL with inner $ \033, this has been modified compared to the original
	# echo '' is raw, "" is execute
	echo '
# set variable identifying the filesystem you work in (used in the prompt below)
set_bash_prompt(){
    fs_mode=$(mount | sed -n -e "s/^\/dev\/.* on \/ .*(\(r[w|o]\).*/\1/p")' | sudo tee -a /etc/bash.bashrc > /dev/null
	
	echo "
    PS1='\[\\033[01;32m\]\u@\h\${fs_mode:+(\$fs_mode)}\[\\033[00m\]:\[\\033[01;34m\]\w\[\\033[00m\]\\$ '
}
alias ro='sudo mount -o remount,ro / ; sudo mount -o remount,ro /boot'
alias rw='sudo mount -o remount,rw / ; sudo mount -o remount,rw /boot'
# setup fancy prompt
PROMPT_COMMAND=set_bash_prompt" | sudo tee -a /etc/bash.bashrc > /dev/null
fi

if [ 0 -eq $( grep -c 'mount -o remount' /etc/bash.bash_logout ) ]; then
  { echo "mount -o remount,ro /" ; echo "mount -o remount,ro /boot"; } | sudo tee -a /etc/bash.bash_logout
fi

#echo "* Configuring kernel to auto reboot on panic."
#echo "kernel.panic = 10" > /etc/sysctl.d/01-panic.conf

echo "* Done! Reboot and hope it will come back up..."