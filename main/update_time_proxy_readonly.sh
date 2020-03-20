#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi

ro=$(mount | sed -n -e "s/^\/dev\/.* on \/ .*(\(r[w|o]\).*/\1/p")
if [ "$ro" = "ro" ]; then
mount -o remount,rw /
fi

# automatically get and set time from the internet (workaround for proxy setting)
date -s "$(wget -qSO- --max-redirect=0 google.vn 2>&1 | grep Date: | cut -d' ' -f5-8)Z"

if [ "$ro" = "ro" ]; then
mount -o remount,ro /
fi

# (c) 2020 Minh-An Dao, Can Tho University