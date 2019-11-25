"""------------------------------------------------------------*-
  Peripheral initialization for Raspberry Pi
  Manipulate 6 IC 74HC595 using C and Subprocess module
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (C) Yasuhiro Ogino 2019
  version 1.00 - 24/11/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import subprocess as subpro
import lcd

pi_dir = "./peripheral_init"

if __name__ == '__main__':
    lcd.begin()
    
    try:
        subpro.Popen([pi_dir], shell=False)
    except KeyboardInterrupt:
        pass