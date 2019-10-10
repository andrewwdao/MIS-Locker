"""------------------------------------------------------------*-
  Peripheral controller for Raspberry Pi
  Manipulate 6 IC 74HC595 using C and Subprocess module
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (C) Yasuhiro Ogino 2019
  version 1.00 - 10/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import subprocess as subpro
import time

pi_dir = "./peripheral_init"
pm1_dir = "./peripheral_main " + "0" + " " + "0" + " " + "0" + " " + "0" + " " + "0" + " " + "0"
pm2_dir = "./peripheral_main " + "12" + " " + "34" + " " + "56" + " " + "12" + " " + "34" + " " + "56"

subpro.Popen([pi_dir], shell=True)
time.sleep(2) # peripheral start up time

while True:
    print('off')
    subpro.Popen([pm1_dir], shell=True)
    time.sleep(1)
    print('on')
    subpro.Popen([pm2_dir], shell=True)
    time.sleep(1)
