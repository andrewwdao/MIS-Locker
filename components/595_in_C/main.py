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
import peripheral as pr
import time

pr.init()

try:
        lok = input('Which Locker? ')
        LOCKER = int(lok)
        while True:
                ans = input('Green (g) or Red (r)? ')
                if ans == 'g':
                        print('Locker on - Green LED on')
                        pr.locker(LOCKER,pr.OPEN)
                        input('Stop? ')
                        pr.locker(LOCKER,pr.CLOSE)
                if ans == 'r':
                        print('Locker busy - Red LED on')
                        pr.locker_nowBusy(LOCKER,pr.ON)
                        input('Stop? ')
                        pr.locker_nowBusy(LOCKER,pr.OFF)
      
except KeyboardInterrupt:
    pass

