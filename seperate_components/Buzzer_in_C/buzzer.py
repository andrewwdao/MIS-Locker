"""*------------------------------------------------------------*-
  Buzzer main functions - python file
  Tested on Gwiot 7304D2 RFID Reader(26 bit Wiegand mode) and RASPBERRY PI 3B+
    (c) Minh-An Dao 2019
  version 1.00 - 28/10/2019
 --------------------------------------------------------------
 *
 * Usage:
 * ./buzzer_main [-d] [delay] [-b] [beep] [-p] [pin]
 *  With:
 *  -delay: buzzer ON time
 *  -beep : times to beep
 *  -pin: new buzzer pin (wiringPi pin)
 *
 --------------------------------------------------------------"""
import subprocess as subpro

TARGET = './buzzer_main'


def beep(delayTime, buzTimes):
    # print('Buzzer ready!')
    subpro.Popen([TARGET, str(delayTime), str(buzTimes)], shell=False)


