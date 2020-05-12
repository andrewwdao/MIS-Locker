#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi

echo "This will set up the admin database for Raspberry Pi's streaming server"

cd app/

# delete old database (admin information)
if [ -f "/home/$(who am i | awk '{print $1}')/system/main/database.db" ] ; then # check if database.db exist or not
	rm -rf /home/$(who am i | awk '{print $1}')/system/main/database.db
fi

# delete old migrations folder
if [ -d "/home/$(who am i | awk '{print $1}')/system/main/migrations" ] ; then  # check if the directory exist or not
	rm -rf /home/$(who am i | awk '{print $1}')/system/main/migrations
fi

# delete old log folder in the app folder
if [ -d "/home/$(who am i | awk '{print $1}')/system/main/logs" ] ; then  # check if the directory exist or not
	rm -rf /home/$(who am i | awk '{print $1}')/system/main/logs
fi

flask db init
flask db migrate -m "users table"
flask db upgrade



echo
echo
echo "Database Done."

## (c) 2020 Minh-An Dao. All right reserved