"""------------------------------------------------------------*-
  LCD application module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  version 1.00 - 02/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
from LCD.LCD_I2C import LCD_I2C

# ---------------------------- Private Parameters:
# -----Address and Screen parameter:
LCD_ADDRESS = 0x27
LCD_WIDTH = 20
LCD_HEIGHT = 4
LCD = None


# ------------------------------ Basic functions ------------------------------
def begin():
    global LCD
    LCD = LCD_I2C(LCD_ADDRESS, LCD_WIDTH, LCD_HEIGHT)
    LCD.backlight()
    LCD.clear()
    LCD.setCursor(2, 0)  # row, column
    LCD.write("SYSTEM  STARTING")
    LCD.setCursor(7, 2)  # row, column
    LCD.write("....")


def pointerPos(options, pointer):
    if options == 3:
        for pos in range(1, options+1):  # go from 1 to (options+1)
            if pos == pointer:
                LCD.setCursor(0, pos)  # row, column
                LCD.write(">")
            else:
                LCD.setCursor(0, pos)  # row, column
                LCD.write(" ")
    elif options == 2:
        for pos in range(1, options+1):  # go from 0 to (options+1)
            if pos == pointer:
                LCD.setCursor(0, pos+1)  # row, column
                LCD.write(">")
            else:
                LCD.setCursor(0, pos+1)  # row, column
                LCD.write(" ")


def clear():
    LCD.clear()


# ------------------------------ User level interfaces ------------------------------
def waitPage():  # user can use RFID or their fingerprint
    LCD.setCursor(4, 0)  # row, column
    LCD.write("SYSTEM READY")
    LCD.setCursor(5, 2)  # row, column
    LCD.write("waiting...")


def welcomePage(name, mssv, locker_num):
    LCD.setCursor(3, 0)  # row, column
    LCD.write("WELCOME TO MIS!")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Name: " + name)
    LCD.setCursor(0, 2)  # row, column
    LCD.write("MSSV: " + mssv)
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Your Locker is " + str(locker_num))


def addExtraInfoPage(name, mssv):
    LCD.setCursor(0, 0)  # row, column
    LCD.write("Name: " + name)
    LCD.setCursor(0, 1)  # row, column
    LCD.write("MSSV: " + mssv)
    LCD.setCursor(2, 2)  # row, column
    LCD.write("New RFID")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("New fingerprint")


def welcomeTempPage(locker_num):
    LCD.setCursor(3, 0)  # row, column
    LCD.write("TEMPORARY USER")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("This is a one-time")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("user only.")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Your Locker is " + str(locker_num))


def unknownIDPage():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("NOT RECOGNISED ID!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Add New ID")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Add Existed ID")


def addFingerPage(number):
    LCD.setCursor(2, 0)  # row, column
    LCD.write("ADD  FINGERPRINT")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Put your finger")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("in position " + str(number))


def addFingerSuccessPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("ADD  FINGERPRINT")
    LCD.setCursor(1, 1)  # row, column
    LCD.write("Fingerprint added!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Press any to return")


def addFingerFailPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("ADD  FINGERPRINT")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


def addRFIDPage():
    LCD.setCursor(6, 0)  # row, column
    LCD.write("ADD RFID")
    LCD.setCursor(3, 2)  # row, column
    LCD.write("Put your RFID")
    LCD.setCursor(3, 3)  # row, column
    LCD.write("in the reader")


def addRFIDSuccessPage():
    LCD.setCursor(6, 0)  # row, column
    LCD.write("ADD RFID")
    LCD.setCursor(4, 1)  # row, column
    LCD.write("RFID added!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Press any to return")


def addRFIDFailPage():
    LCD.setCursor(6, 0)  # row, column
    LCD.write("ADD RFID")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


def addInfoPage():
    LCD.setCursor(5, 0)  # row, column
    LCD.write("ADD NEW INFO")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Connect to MIS-CTU")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("wifi & open browser")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("to: mis-locker.ctu")


# ------------------------------ Admin level interfaces ------------------------------
def mainDatabasePage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADMIN MENU:")
    LCD.setCursor(2, 1)  # row, column
    LCD.write("1. Export Database")  # export will export everything
    LCD.setCursor(2, 2)  # row, column
    LCD.write("2. Import Database")  # import will have 2 options: append and override
    LCD.setCursor(2, 3)  # row, column
    LCD.write("3. Clear Database")  #


def exportSuccessPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("EXPORT DATABASE")
    LCD.setCursor(7, 1)  # row, column
    LCD.write("Done!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Press any to return")


def exportFailPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("EXPORT DATABASE")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


def importPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("IMPORT DATABASE")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("1. Append database")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("2. New database")


def importSuccessPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("IMPORT DATABASE")
    LCD.setCursor(7, 1)  # row, column
    LCD.write("Done!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Press any to return")


def importFailPage():
    LCD.setCursor(2, 0)  # row, column
    LCD.write("IMPORT DATABASE")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


def mainLockerPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADMIN MENU:")
    LCD.setCursor(2, 1)  # row, column
    LCD.write("4. Info Locker")  # check any locker that has information in


def infoLockerPage(name, mssv):
    LCD.setCursor(4, 0)  # row, column
    LCD.write("INFO LOCKER")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Name: " + name)
    LCD.setCursor(0, 2)  # row, column
    LCD.write("MSSV: " + mssv)
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Unlock?")


def infoLockerTempPage():
    LCD.setCursor(4, 0)  # row, column
    LCD.write("INFO LOCKER")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Temporary User")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Unlock?")
