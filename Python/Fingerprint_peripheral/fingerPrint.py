"""------------------------------------------------------------*-
  fingerPrint module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (C) Bastian Raschke 2015
  version 1.00 - 09/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
from pyfingerprint.pyfingerprint import PyFingerprint
import RPi.GPIO as GPIO  # default as BCM mode!
import time

# ---------------------------- Private Parameters:
# -----Starting parameter:
FINGER_PORT = '/dev/ttyUSB0'
FINGER_BAUDRATE = 57600
FINGER_ADDRESS = 0xFFFFFFFF
FINGER_PASSWORD = 0x00000000
TOUCH_PIN = 10  # BCM Mode
WAIT_TIME = 5  # waiting time between first and second scan of enroll func
DEBOUNCE = 10
START_CHECKING = False
Finger = None


# ------------------------------ Basic functions ------------------------------
def begin():  # Tries to initialize the sensor
    global Finger
    try:
        # pulled up to avoid false detection.
        # So we'll be setting up falling edge detection
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TOUCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        Finger = PyFingerprint(FINGER_PORT, FINGER_BAUDRATE, FINGER_ADDRESS, FINGER_PASSWORD)
        if not Finger.verifyPassword():
            raise ValueError('Password for the Fingerprint module is wrong!')
        # Gets some sensor information
        print('Currently used templates: ' + str(Finger.getTemplateCount()) + '/' + str(Finger.getStorageCapacity()))
        return True
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        return False


def enroll():
    try:
        print('Waiting for finger...')
        while not Finger.readImage():  # Wait for incoming finger is read
            pass

        # Converts read image to characteristics and stores it in charbuffer 1
        Finger.convertImage(0x01)

        # Checks if finger is already enrolled
        result = Finger.searchTemplate()
        positionNumber = result[0]
        if positionNumber >= 0:
            # NEED TO ADD ALGORITHM HERE
            print('Finger already exists at #' + str(positionNumber))
            return ["EXISTED", positionNumber]

        print('Done.')
        time.sleep(WAIT_TIME)
        print('Second time. Waiting for finger...')

        while not Finger.readImage():  # Wait that finger is read again
            pass

        # Converts read image to characteristics and stores it in charbuffer 2
        Finger.convertImage(0x02)

        # Compares the charbuffers
        if not Finger.compareCharacteristics():
            return ["FAILED", 0]

        # Pass second read. Creates the corresponding template
        Finger.createTemplate()

        # Saves the template at a new position number
        positionNumber = Finger.storeTemplate()
        print('Finger enrolled successfully!')
        print('New template position #' + str(positionNumber))
        return ["DONE", positionNumber]
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return ["ERROR", e]


def delete(pos):  # Delete the template of the finger
    try:
        if Finger.deleteTemplate(pos):
            print('Template deleted!')
            return True
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        return False


def scan():  # Search for the incoming finger in database
    try:
        print('Waiting for finger...')
        while not Finger.readImage():  # Wait for incoming finger is read
            pass

        # Converts read image to characteristics and stores it in charbuffer 1
        Finger.convertImage(0x01)

        # Search for template info in the database of the R301T
        result = Finger.searchTemplate()
        positionNumber = result[0]
        accuracyScore = result[1]

        if positionNumber == -1:
            print('No match found!')
            print(["NOT MATCHED", 0])
            return ["NOT MATCHED", 0]
        else:
            print('Template found at #' + str(positionNumber))
            print('Accuracy: ' + str(accuracyScore))
            print(["MATCHED", positionNumber])
            return ["MATCHED", positionNumber]
    except Exception as e:
        print('Operation failed!')
        print('Exception message: ' + str(e))
        print(["ERROR", e])
        return ["ERROR", e]


def touchISR(channel):
    global START_CHECKING
    START_CHECKING = True


def activate():
    GPIO.add_event_detect(TOUCH_PIN, GPIO.FALLING, callback=touchISR, bouncetime=DEBOUNCE)


def deactivate():
    GPIO.remove_event_detect(TOUCH_PIN)


def check():
    global START_CHECKING
    if START_CHECKING:
        START_CHECKING = False
        return scan()
    return ["NO DATA", 0]
