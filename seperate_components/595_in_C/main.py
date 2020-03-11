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

LOCKER = 1
TIME = 3
try:
#    time.sleep(3)
        while True:
                ans = input('Green (g) or Red (r)?')
                if ans == 'g':
                        print('Locker on - Green LED on')
                        pr.locker(LOCKER,pr.OPEN)
                        time.sleep(TIME)
                        pr.locker(LOCKER,pr.CLOSE)
                if ans == 'r':
                        print('Locker busy - Red LED on')
                        pr.locker_nowBusy(LOCKER,pr.ON)
                        time.sleep(TIME)
                        pr.locker_nowBusy(LOCKER,pr.OFF)
                
        
        # time.sleep(1)
        # print('Locker off')
        # pr.locker(LOCKER,pr.CLOSE)
        # time.sleep(1)
        # print('Locker busy')
        # pr.locker_nowBusy(LOCKER,pr.ON)
        # time.sleep(1)
        # print('Locker off')
        # pr.locker_nowBusy(LOCKER,pr.OFF)
        # time.sleep(1)
#        print('Locker busy')
#        per.lock01_busy(per.ON)
#        time.sleep(1)
#        print('Locker free')
#        per.lock01_busy(per.OFF)
#        time.sleep(1)
#        print('Locker 03 on')
#        per.lock03(per.ON)
#        time.sleep(1)
#        print('Locker 03 off')
#        per.lock03(per.OFF)
#        time.sleep(1)
#        print('Locker 04 on')
#        per.lock04(per.ON)
#        time.sleep(1)
#        print('Locker 04 off')
#        per.lock04(per.OFF)
#        time.sleep(1)
#        print('Locker 05 on')
#        per.lock05(per.ON)
#        time.sleep(1)
#        print('Locker 05 off')
#        per.lock05(per.OFF)
#        time.sleep(1)
#        print('Locker 06 on')
#        per.lock06(per.ON)
#        time.sleep(1)
#        print('Locker 06 off')
#        per.lock06(per.OFF)
#        time.sleep(1)
#        print('Locker 07 on')
#        per.lock07(per.ON)
#        time.sleep(1)
#        print('Locker 07 off')
#        per.lock07(per.OFF)
#        time.sleep(1)
#        print('Locker 08 on')
#        per.lock08(per.ON)
#        time.sleep(1)
#        print('Locker 08 off')
#        per.lock08(per.OFF)
#        time.sleep(1)
#        print('Locker 09 on')
#        per.lock09(per.ON)
#        time.sleep(1)
#        print('Locker 09 off')
#        per.lock09(per.OFF)
#        time.sleep(1)
#        print('Locker 10 on')
#        per.lock10(per.ON)
#        time.sleep(1)
#        print('Locker 10 off')
#        per.lock10(per.OFF)
#        time.sleep(1)
except KeyboardInterrupt:
    pass

