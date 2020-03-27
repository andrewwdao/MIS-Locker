"""------------------------------------------------------------*-
  Buttons and Switches module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2020
  version 1.00 - 27/03/2020
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import RPi.GPIO as GPIO  # default as BCM mode!
import time

# ---------------------------- Private Parameters:
DEBOUNCE = 500  # xxx second
# -----Pinout
UP_BUTTON = 5
DOWN_BUTTON = 13 
OK_BUTTON = 12
CANCEL_BUTTON = 25
# ----- Button state
UP_STATE = False
DOWN_STATE = False
OK_STATE = False
CANCEL_STATE = False


def __upISR(channel):
    global UP_STATE
    UP_STATE = True

def __downISR(channel):
    global DOWN_STATE
    DOWN_STATE = True

def __okISR(channel):
    global OK_STATE
    OK_STATE = True

def __cancelISR(channel):
    global CANCEL_STATE
    CANCEL_STATE = True


def init():

    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(UP_BUTTON, GPIO.FALLING, callback=__upISR, bouncetime=DEBOUNCE)

    GPIO.setup(DOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(DOWN_BUTTON, GPIO.FALLING, callback=__downISR, bouncetime=DEBOUNCE)

    GPIO.setup(OK_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(OK_BUTTON, GPIO.FALLING, callback=__okISR, bouncetime=DEBOUNCE)

    GPIO.setup(CANCEL_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(CANCEL_BUTTON, GPIO.FALLING, callback=__cancelISR, bouncetime=DEBOUNCE)
 

def read():
    global UP_STATE
    global DOWN_STATE
    global OK_STATE
    global CANCEL_STATE
    if OK_STATE:
        OK_STATE = False
        return "BUT_OK"
    if CANCEL_STATE:
        CANCEL_STATE = False
        return "BUT_CANCEL"
    if UP_STATE:
        UP_STATE = False
        return "BUT_UP"
    if DOWN_STATE:
        DOWN_STATE = False
        return "BUT_DOWN"


