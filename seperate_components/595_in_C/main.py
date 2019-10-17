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
import peripheral as per
import time

per.init()

try:
    while True:
        print('Locker 01 on')
        per.lock01(per.ON)
        time.sleep(1)
        print('Locker 01 off')
        per.lock01(per.OFF)
        time.sleep(1)
        print('Locker 02 on')
        per.lock02(per.ON)
        time.sleep(1)
        print('Locker 02 off')
        per.lock02(per.OFF)
        time.sleep(1)
        print('Locker 03 on')
        per.lock03(per.ON)
        time.sleep(1)
        print('Locker 03 off')
        per.lock03(per.OFF)
        time.sleep(1)
        print('Locker 04 on')
        per.lock04(per.ON)
        time.sleep(1)
        print('Locker 04 off')
        per.lock04(per.OFF)
        time.sleep(1)
        print('Locker 05 on')
        per.lock05(per.ON)
        time.sleep(1)
        print('Locker 05 off')
        per.lock05(per.OFF)
        time.sleep(1)
        print('Locker 06 on')
        per.lock06(per.ON)
        time.sleep(1)
        print('Locker 06 off')
        per.lock06(per.OFF)
        time.sleep(1)
        print('Locker 07 on')
        per.lock07(per.ON)
        time.sleep(1)
        print('Locker 07 off')
        per.lock07(per.OFF)
        time.sleep(1)
        print('Locker 08 on')
        per.lock08(per.ON)
        time.sleep(1)
        print('Locker 08 off')
        per.lock08(per.OFF)
        time.sleep(1)
        print('Locker 09 on')
        per.lock09(per.ON)
        time.sleep(1)
        print('Locker 09 off')
        per.lock09(per.OFF)
        time.sleep(1)
        print('Locker 10 on')
        per.lock10(per.ON)
        time.sleep(1)
        print('Locker 10 off')
        per.lock10(per.OFF)
        time.sleep(1)
except KeyboardInterrupt:
    pass

