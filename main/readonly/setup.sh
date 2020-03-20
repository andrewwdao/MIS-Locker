#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi

echo ""
echo "This script will turn this operating system into a read-only one."
echo "Back up should be made where needed before proceed."
echo "Designed specifically for MISlocker."
echo "Ported from Ways project at: https://gitlab.com/larsfp/rpi-readonly"
echo -n "Confirm to install? [Y/N]"

read input

if ! [ $input == "y" ] || [ $input == "Y" ]; then
	{ echo "Exiting..."; exit 1; }
fi

echo "Installing..."

# automatically get and set time from the internet (workaround for proxy setting at MIS-CTU)
date -s "$(wget -qSO- --max-redirect=0 google.vn 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

apt-get update && apt-get upgrade -y

echo "* Installing some needed software..."
apt-get install -y busybox-syslogd ntp # watchdog

echo "*Removing some unneeded software..."
apt-get remove -y --purge wolfram-engine triggerhappy anacron logrotate dphys-swapfile xserver-common lightdm rsyslog
apt-get autoremove --purge -y
systemctl disable x11-common

# update all the kept-back if existed  # # https://askubuntu.com/questions/601/the-following-packages-have-been-kept-back-why-and-how-do-i-solve-it
apt-get --with-new-pkgs upgrade -y
	
echo "* Changing boot up parameters..."
# systemd-hostnamed uses a private temp folder on the root fs by default
# let's rather use /tmp
sed -i.bck 's/PrivateTmp=yes/PrivateTmp=no/' /lib/systemd/system/systemd-hostnamed.service

if [ 0 -eq $( grep -c 'fastboot noswap ro' /boot/cmdline.txt ) ]; then # check if the phrase "fastboot noswap ro" existed in the file or not
	echo "*** Disable swap and filesystem check and set it to read-only..."
	sed -i.bck '$s/$/ fastboot noswap ro/' /boot/cmdline.txt
	sed -i.bck 's/fsck.repair=yes/fsck.mode=skip/' /boot/cmdline.txt

fi

echo "* Move resolv.conf to tmpfs..."
if ! [ -f "/tmp/dhcpcd.resolv.conf" ] ; then
	mv /etc/resolv.conf /tmp/dhcpcd.resolv.conf
	ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf
fi

#echo "* Moving pids and other files to tmpfs"
#sed -i.bak '/PIDFile/c\PIDFile=\/run\/dhcpcd.pid' /etc/systemd/system/dhcpcd5.service

rm /var/lib/systemd/random-seed && \
  ln -s /tmp/random-seed /var/lib/systemd/random-seed

if [ 0 -eq $( grep -c "ExecStartPre=/bin/echo '' >/tmp/random-seed" /lib/systemd/system/systemd-random-seed.service ) ]; then # check if the phrase "ExecStartPre=/bin/echo '' >/tmp/random-seed" existed in the file or not
	sed -i.bck "/RemainAfterExit=yes/a ExecStartPre=\/bin\/echo '' >\/tmp\/random-seed" /lib/systemd/system/systemd-random-seed.service   # append new line after a pattern. ref: https://unix.stackexchange.com/questions/121161/how-to-insert-text-after-a-certain-string-in-a-file
fi

systemctl daemon-reload

if [ 0 -eq $( grep -c "mount -o remount,rw" /etc/cron.hourly/fake-hwclock ) ]; then # check if the phrase "mount -o remount,rw" existed in the file or not
  cp /etc/cron.hourly/fake-hwclock /etc/cron.hourly/fake-hwclock.backup
  cat ./fake-hwclock.addon >> /etc/cron.hourly/fake-hwclock
fi

sed -i.bak '/driftfile/c\driftfile /tmp\/ntp.drift' /etc/ntp.conf

echo "* Setting up tmpfs for lightdm, in case this isn't a headless system."
ln -fs /tmp/.Xauthority /home/$(who am i | awk '{print $1}')/.Xauthority
ln -fs /tmp/.xsession-errors /home/$(who am i | awk '{print $1}')/.xsession-errors

echo "* Setting fs as ro in fstab..."
if [ 0 -eq $( grep -c ',ro' /etc/fstab ) ]; then
  sed -i.bak "/boot/ s/defaults/defaults,ro/g" /etc/fstab
  sed -i "/ext4/ s/defaults/defaults,ro/g" /etc/fstab

  echo "
  tmpfs           /tmp             tmpfs   nosuid,nodev         0       0
  tmpfs           /var/log         tmpfs   nosuid,nodev         0       0
  tmpfs           /var/tmp         tmpfs   nosuid,nodev         0       0
  tmpfs           /var/lib/dhcpcd5 tmpfs   nosuid,nodev         0       0
" >> /etc/fstab
fi

echo "* Modifying bashrc..."
if [ 0 -eq $( grep -c 'mount -o remount' /etc/bash.bashrc ) ]; then
  cat ./bash.bashrc.addon >> /etc/bash.bashrc
fi

touch /etc/bash.bash_logout
if [ 0 -eq $( grep -c 'mount -o remount' /etc/bash.bash_logout ) ]; then
  cat ./bash.bash_logout.addon >> /etc/bash.bash_logout
fi

echo "* Configuring kernel to auto reboot on panic..."
echo "kernel.panic = 10" > /etc/sysctl.d/01-panic.conf

echo "* Disabling apt-daily and apt-daily-upgrade services"
systemctl stop systemd-tmpfiles-clean.timer apt-daily.timer apt-daily-upgrade.timer
systemctl disable apt-daily.service apt-daily.timer
systemctl disable apt-daily-upgrade.service apt-daily-upgrade.timer
systemctl disable systemd-tmpfiles-clean.service systemd-tmpfiles-clean.timer
systemctl stop systemd-tmpfiles-clean.timer apt-daily.timer apt-daily-upgrade.timer
systemctl disable systemd-tmpfiles-clean.timer systemd-tmpfiles-clean apt-daily.timer apt-daily-upgrade.timer
# dphys-swapfile is already removed. systemctl disable dphys-swapfile && rm /var/swap
systemctl mask systemd-update-utmp systemd-update-utmp-runlevel systemd-rfkill systemd-rfkill.socket

echo ""
echo "* Done! Reboot and hope it will come back up..."

# ref: https://gitlab.com/larsfp/rpi-readonly
# ref: https://k3a.me/how-to-make-raspberrypi-truly-read-only-reliable-and-trouble-free/
# ref: https://hallard.me/raspberry-pi-read-only/
# ref: https://mad-tinkerer.me/raspberry-pi/read-only-root-filesystem-debian-buster/

# append ref
# ref: https://unix.stackexchange.com/questions/121161/how-to-insert-text-after-a-certain-string-in-a-file
# ref: https://unix.stackexchange.com/questions/77277/how-to-append-multiple-lines-to-a-file
# ref: https://www.golinuxhub.com/2017/06/sed-insert-word-after-match-in-middle.html
# ref: https://stackoverflow.com/questions/35252285/insert-text-with-sed-on-the-same-line-that-pattern-search


# (c) 2020 Minh-An Dao, Can Tho University