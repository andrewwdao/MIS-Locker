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
from rfid import Gwiot_7304D2 as RFID

try:
    rfid = RFID()
    print('RFID System ready!')
    while True:
        if rfid.available():
            print(rfid.read())
            print('done!')

except KeyboardInterrupt:
    pass
