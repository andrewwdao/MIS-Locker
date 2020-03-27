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
# ACTIVATE_MODULE02 = False
DEBOUNCE = 100  # xxx second
# -----Address and Screen parameter:
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
    return "NO_CHANGE"


    # def read(self):
    #     last_status = self.status
    #     self.status = self.__read()
    #     time.sleep(DEBOUNCE)  # debounce for DEBOUNCE time
    #     if self.status != last_status or self.status == "BUT_NO_PRESS":
    #         return self.status
    #     else:
    #         return "NO_CHANGE"




# class adc_switches(adc_read):
#     def __init__(self):
#         super().__init__()
#         if ACTIVATE_MODULE02:  # Module02 also activated
#             self.switchesM1 = AnalogIn(self.ads, SWITCH_M1)
#             self.switchesM2 = AnalogIn(self.ads, SWITCH_M2)
#         else:  # only Module01 is activated
#             self.switchesM1 = AnalogIn(self.ads, SWITCH_M1)

#     def read(self):
#         current_valM1 = self.switchesM1.value
#         if ACTIVATE_MODULE02:
#             current_valM2 = self.switchesM2.value
#             if (ALL_CLOSED_MIN < current_valM1 < ALL_CLOSED_MAX) and \
#                (ALL_CLOSED_MIN < current_valM2 < ALL_CLOSED_MAX):  # all doors closed
#                 return "ALL_CLOSED"
#             # first check module02
#             elif (current_valM1 < ALL_CLOSED_MIN) and \
#                  (current_valM2 < ALL_CLOSED_MIN):  # some doors are open
#                 return "OPEN"
#         else:  # if only module 01 is activated
#             if ALL_CLOSED_MIN < current_valM1 < ALL_CLOSED_MAX:  # all doors closed
#                 return "ALL_CLOSED"
#             # now check Module01
#             elif current_valM1 < ALL_CLOSED_MIN: # some doors are open
#                 return "OPEN"
#         # if still nothing return, then must be some error
#         return "ERROR"


#     def readRawM1(self):
#         return self.switchesM1.value

#     def readRawM2(self):
#         return self.switchesM2.value


# ---------- Deprecated 

# class adc_switches(adc_read):
#     def __init__(self):
#         super().__init__()
#         if ACTIVATE_MODULE02:  # Module02 also activated
#             self.switchesM1 = AnalogIn(self.ads, SWITCH_M1)
#             self.switchesM2 = AnalogIn(self.ads, SWITCH_M2)
#         else:  # only Module01 is activated
#             self.switchesM1 = AnalogIn(self.ads, SWITCH_M1)

#     def read(self):
#         current_valM1 = self.switchesM1.value
#         if ACTIVATE_MODULE02:
#             current_valM2 = self.switchesM2.value
#             if (ALL_CLOSED_MIN < current_valM1 < ALL_CLOSED_MAX) and \
#                (ALL_CLOSED_MIN < current_valM2 < ALL_CLOSED_MAX):  # all doors closed
#                 return "ALL_CLOSED"
#             # first check module02
#             if DOOR11_MIN < current_valM2 < DOOR11_MAX:  # door11
#                 return "DOOR11"
#             if DOOR12_MIN < current_valM2 < DOOR12_MAX:  # door12
#                 return "DOOR12"
#             if DOOR13_MIN < current_valM2 < DOOR13_MAX:  # door13
#                 return "DOOR13"
#             if DOOR14_MIN < current_valM2 < DOOR14_MAX:  # door14
#                 return "DOOR14"
#             if DOOR15_MIN < current_valM2 < DOOR15_MAX:  # door15
#                 return "DOOR15"
#             if DOOR16_MIN < current_valM2 < DOOR16_MAX:  # door16
#                 return "DOOR16"
#             if DOOR17_MIN < current_valM2 < DOOR17_MAX:  # door17
#                 return "DOOR17"
#             if DOOR18_MIN < current_valM2 < DOOR18_MAX:  # door18
#                 return "DOOR18"
#             if DOOR19_MIN < current_valM2 < DOOR19_MAX:  # door19
#                 return "DOOR19"
#             if DOOR20_MIN < current_valM2 < DOOR20_MAX:  # door20
#                 return "DOOR20"
#         else:
#             if ALL_CLOSED_MIN < current_valM1 < ALL_CLOSED_MAX:  # all doors closed
#                 return "ALL_CLOSED"
#         # now check Module01
#         if DOOR01_MIN < current_valM1 < DOOR01_MAX:  # door01
#             return "DOOR01"
#         if DOOR02_MIN < current_valM1 < DOOR02_MAX:  # door02
#             return "DOOR02"
#         if DOOR03_MIN < current_valM1 < DOOR03_MAX:  # door03
#             return "DOOR03"
#         if DOOR04_MIN < current_valM1 < DOOR04_MAX:  # door04
#             return "DOOR04"
#         if DOOR05_MIN < current_valM1 < DOOR05_MAX:  # door05
#             return "DOOR05"
#         if DOOR06_MIN < current_valM1 < DOOR06_MAX:  # door06
#             return "DOOR06"
#         if DOOR07_MIN < current_valM1 < DOOR07_MAX:  # door07
#             return "DOOR07"
#         if DOOR08_MIN < current_valM1 < DOOR08_MAX:  # door08
#             return "DOOR08"
#         if DOOR09_MIN < current_valM1 < DOOR09_MAX:  # door09
#             return "DOOR09"
#         if DOOR10_MIN < current_valM1 < DOOR10_MAX:  # door10
#             return "DOOR10"
#         # if still nothing return, then must be some error
#         return "ERROR"

