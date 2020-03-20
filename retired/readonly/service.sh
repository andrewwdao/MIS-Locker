#!/bin/bash

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
# Restart=yes
# must set user to root to execute all functions and peripherals
User=root
# SIGINT is translated as a KeyboardInterrupt exception by Python.
# default kill signal is SIGTERM which doesn't raise an exception in Python.
# KillSignal=SIGINT
# Additional commands that are executed after the service is stopped. ref: https://www.freedesktop.org/software/systemd/man/systemd.service.html
ExecStopPost=sudo python3 -u syshalt.py

 
[Install]
WantedBy=sysinit.target multi-user.target
" > ./hello.service