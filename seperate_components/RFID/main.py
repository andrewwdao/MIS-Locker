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
# !/usr/bin/env python

# green/data0 is pin 22
# white/data1 is pin 7
import time
import RPi.GPIO as GPIO

D0 = 9
D1 = 10
bits = ''
timeout = 5

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(D0, GPIO.IN)
GPIO.setup(D1, GPIO.IN)


def one(channel):
    global bits
    bits += '1'


def zero(channel):
    global bits
    bits += '0'


GPIO.add_event_detect(D0, GPIO.FALLING, callback=zero)
GPIO.add_event_detect(D1, GPIO.FALLING, callback=one)

print("Present Card")
try:
    while True:
        if len(bits) == 32:
            # time.sleep(0.1)
            # print "Binary:",bits
            print("Decimal:", int(str(bits), 2))
            print("Hex:",hex(int(str(bits), 2)))
            bits = '0'
            # time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print
    "Clean Exit By user"

GPIO.cleanup()
