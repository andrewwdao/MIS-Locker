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

# ---------------------------- Private Parameters:
# -----Starting parameter:
FINGER_PORT = '/dev/ttyUSB0'
FINGER_BAUDRATE = 57600
FINGER_ADDRESS = 0xFFFFFFFF
FINGER_PASSWORD = 0x00000000
myFinger = PyFingerprint(FINGER_PORT, FINGER_BAUDRATE, FINGER_ADDRESS, FINGER_PASSWORD)

# ------------------------------ Basic functions ------------------------------
def begin():
    # Tries to initialize the sensor
    try:
        myFinger = PyFingerprint(FINGER_PORT, FINGER_BAUDRATE, FINGER_ADDRESS, FINGER_PASSWORD)
        if not myFinger.verifyPassword():
            raise ValueError('Password for the Fingerprint module is wrong!')
    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        exit(1)
    # Gets some sensor information
    print('Currently used templates: ' + str(myFinger.getTemplateCount()) + '/' + str(myFinger.getStorageCapacity()))


# Tries to show a template index table page
try:
    page = input('Please enter the index page (0, 1, 2, 3) you want to see: ')
    page = int(page)

    tableIndex = myFinger.getTemplateIndex(page)

    for i in range(0, len(tableIndex)):
        print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))

except Exception as e:
    print('Operation failed!')
    print('Exception message: ' + str(e))
    exit(1)
