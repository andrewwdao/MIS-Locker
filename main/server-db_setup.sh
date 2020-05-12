#!/bin/bash

set -eu -o pipefail # fail on error , debug all lines

if [ 'root' != $( whoami ) ] ; then
  echo "Please run as root! ( sudo ${0} )"
  exit 1;
fi

echo "This will set up the admin database for Raspberry Pi's streaming server"

cd app/

# delete old database (admin information)
if [ -f "./database.db" ] ; then # check if database.db exist or not
	rm -rf database.db
fi

# delete old migrations folder
if [ -d "./migrations" ] ; then  # check if the directory exist or not
	rm -rf migrations
fi

# delete old log folder in the app folder
if [ -d "./logs" ] ; then  # check if the directory exist or not
	rm -rf logs
fi

# delete old log again in the main folder
if [ -d "../logs" ] ; then  # check if the directory exist or not
	rm -rf ../logs
fi

flask db init
flask db migrate -m "users table"
flask db upgrade



python3 ../server_admin-init.py

echo
echo
echo "Database Done."

## (c) 2020 Minh-An Dao. All right reserved