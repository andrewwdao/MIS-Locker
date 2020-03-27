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
M1_SWITCH = 20
M2_SWITCH = 21 
# ----- Button state
M1_STATE = False
M2_STATE = False


def __m1openISR(channel):
    global M1_STATE
    M1_STATE = True
    GPIO.remove_event_detect(M1_SWITCH)
    GPIO.add_event_detect(M1_SWITCH, GPIO.RISING, callback=__m1closeISR, bouncetime=DEBOUNCE)

def __m1closeISR(channel):
    global M1_STATE
    M1_STATE = False
    GPIO.remove_event_detect(M1_SWITCH)
    GPIO.add_event_detect(M1_SWITCH, GPIO.FALLING, callback=__m1openISR, bouncetime=DEBOUNCE)

def __m2openISR(channel):
    global M2_STATE
    M2_STATE = True
    GPIO.remove_event_detect(M2_SWITCH)
    GPIO.add_event_detect(M2_SWITCH, GPIO.RISING, callback=__m2closeISR, bouncetime=DEBOUNCE)

def __m2closeISR(channel):
    global M2_STATE
    M2_STATE = False
    GPIO.remove_event_detect(M2_SWITCH)
    GPIO.add_event_detect(M2_SWITCH, GPIO.FALLING, callback=__m2openISR, bouncetime=DEBOUNCE)
    
def init():
    # prevent double init
    GPIO.cleanup()

    GPIO.setmode(GPIO.BCM)


    GPIO.setup(M1_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(M1_SWITCH, GPIO.FALLING, callback=__m1openISR, bouncetime=DEBOUNCE)
    
    GPIO.setup(M2_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(M2_SWITCH, GPIO.FALLING, callback=__m2openISR, bouncetime=DEBOUNCE)
    

def read():
    if M1_STATE | M2_STATE:
        return "OPEN"
    else:
        return "ALL_CLOSED"


# def read():
#     if M1_STATE:
#         return "M1_OPEN"
#     elif M2_STATE:
#         return "M2_OPEN"
#     else:
#         return "ALL_CLOSED"


