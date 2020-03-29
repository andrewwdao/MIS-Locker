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
import subprocess as subpro

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


def waitPage_normal():  # user can use RFID or their fingerprint to access
    LCD.setCursor(1, 0)  # row, column
    LCD.write("   LOCKER READY  ")
    LCD.setCursor(5, 2)  # row, column
    LCD.write("waiting...")


def waitPage_system():  # user can use RFID or their fingerprint to access
    LCD.setCursor(1, 0)  # row, column
    LCD.write("SYSTEM INFO READY")
    LCD.setCursor(5, 2)  # row, column
    LCD.write("waiting...")


def waitforDoorClose(): # wait for user to close the door
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Please shut the door")


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


# ------------------------------ System close - error ------------------------------
def systemClosedPage():  # system closed page
    LCD = LCD_I2C(LCD_ADDRESS, LCD_WIDTH, LCD_HEIGHT)
    LCD.backlight()
    LCD.clear()
    LCD.setCursor(1, 0)  # row, column
    LCD.write("   LOCKER CLOSED   ")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("please return later")
    LCD.setCursor(8, 3)  # row, column
    LCD.write("...")


def systemErrorPage():  # system error page
    LCD = LCD_I2C(LCD_ADDRESS, LCD_WIDTH, LCD_HEIGHT)
    LCD.backlight()
    LCD.clear()
    LCD.setCursor(0, 0)  # row, column
    LCD.write("    LOCKER ERROR    ")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("please contact admin")
    LCD.setCursor(8, 3)  # row, column
    LCD.write("...")


# ------------------------------ User level interfaces ------------------------------
def welcomePage(name, mssv, locker_num):
    LCD.setCursor(3, 0)  # row, column
    LCD.write("WELCOME TO MIS!")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Name: " + name)
    LCD.setCursor(0, 2)  # row, column
    LCD.write("MSSV: " + mssv)
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Your Locker is " + str(locker_num))


def welcomeTempPage(locker_num):
    LCD.setCursor(3, 0)  # row, column
    LCD.write("TEMPORARY USER")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("This is a one-time")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("user only.")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Your Locker is " + str(locker_num))


def outOfVacancyPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("DEAR USER")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("We are out of")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("vacancy. Sorry!")


def returnPage(name, locker_num):
    LCD.setCursor(0, 0)  # row, column
    LCD.write("Hello " + name + "!")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("Your Locker is " + str(locker_num))
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Unlocked!")


def returnTempPage(locker_num):
    LCD.setCursor(0, 0)  # row, column
    LCD.write("Hello User!")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("Your Locker is " + str(locker_num))
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Unlocked!")


def questionPage():
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Continue using?")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Yes")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("No (Default)")


def continueUsingPage():
    LCD.setCursor(0, 1)  # row, column
    LCD.write("YES command received")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Your locker remained")


def changeInfoPage(name):
    LCD.setCursor(0, 0)  # row, column
    LCD.write("Hello " + name)
    LCD.setCursor(2, 1)  # row, column
    LCD.write("Change name/MSSV")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Change RFID")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Change Finger")


def unknownIDPage():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("NOT RECOGNISED ID!")
    LCD.setCursor(2, 1)  # row, column
    LCD.write("Add New ID")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("One-time User")
    

def cancelNewUserPage():
    LCD.setCursor(4, 0)  # row, column
    LCD.write("ADD NEW USER")
    LCD.setCursor(6, 2)  # row, column
    LCD.write("CANCELED")


# ================================================ FINGERPRINT ======================================
def addFingerPage01():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD USER:FINGERPRINT")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Put your finger")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("in the scanner")


def addFingerPage02():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD USER:FINGERPRINT")
    LCD.setCursor(8, 3)  # row, column
    LCD.write("Done")


def addFingerPage03():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD USER:FINGERPRINT")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Put your finger in")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("the scanner again")


def addFingerSuccessPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD USER:FINGERPRINT")
    LCD.setCursor(1, 1)  # row, column
    LCD.write("Fingerprint added!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Press any to return")


def addFingerExistedPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD USER:FINGERPRINT")
    LCD.setCursor(1, 1)  # row, column
    LCD.write("Fingerprint exised!")
    LCD.setCursor(1, 3)  # row, column
    LCD.write("Please check again")


def addFingerFailPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD USER:FINGERPRINT")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


def changeFingerPage01():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("CHANGE FINGERPRINT")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Put your finger")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("in the scanner")


def changeFingerPage02():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("CHANGE FINGERPRINT")
    LCD.setCursor(8, 3)  # row, column
    LCD.write("Done")


def changeFingerPage03():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("CHANGE FINGERPRINT")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Put your finger in")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("the scanner again")


def changeFingerSuccessPage():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("CHANGE FINGERPRINT")
    LCD.setCursor(1, 1)  # row, column
    LCD.write("Fingerprint added!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Press any to return")


def changeFingerExistedPage():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("CHANGE FINGERPRINT")
    LCD.setCursor(1, 1)  # row, column
    LCD.write("Fingerprint exised!")
    LCD.setCursor(1, 3)  # row, column
    LCD.write("Please check again")


def changeFingerFailPage():
    LCD.setCursor(1, 0)  # row, column
    LCD.write("CHANGE FINGERPRINT")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


# ================================================ RFID ======================================
def addRFIDPage():
    LCD.setCursor(3, 0)  # row, column
    LCD.write("ADD USER: RFID")
    LCD.setCursor(3, 2)  # row, column
    LCD.write("Put your RFID")
    LCD.setCursor(3, 3)  # row, column
    LCD.write("in the reader")


def addRFIDSuccessPage():
    LCD.setCursor(3, 0)  # row, column
    LCD.write("ADD USER: RFID")
    LCD.setCursor(4, 1)  # row, column
    LCD.write("RFID added!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Please press OK")


def addRFIDFailPage():
    LCD.setCursor(3, 0)  # row, column
    LCD.write("ADD USER: RFID")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")


def changeRFIDPage():
    LCD.setCursor(4, 0)  # row, column
    LCD.write("CHANGE RFID")
    LCD.setCursor(3, 2)  # row, column
    LCD.write("Put your RFID")
    LCD.setCursor(3, 3)  # row, column
    LCD.write("in the reader")


def changeRFIDSuccessPage():
    LCD.setCursor(4, 0)  # row, column
    LCD.write("CHANGE RFID")
    LCD.setCursor(4, 1)  # row, column
    LCD.write("RFID added!")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Please press OK")


def changeRFIDFailPage():
    LCD.setCursor(4, 0)  # row, column
    LCD.write("CHANGE RFID")
    LCD.setCursor(6, 1)  # row, column
    LCD.write("Failed!")
    LCD.setCursor(2, 2)  # row, column
    LCD.write("Retry")
    LCD.setCursor(2, 3)  # row, column
    LCD.write("Cancel")
# ================================================ INFOMATION ======================================

def addNewInfo():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADD NEW INFO:Connect")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("to MIS-CTU wifi & ")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("open browser to")
    LCD.setCursor(0, 3)  # row, column
    my_ip = subpro.check_output(["hostname", "-I"]).decode("utf-8")[:-2]+":7497"
    LCD.write(my_ip) # get current ip address


def confirmChangeInfo():
    LCD.setCursor(4, 0)  # row, column
    LCD.write("CHANGE INFO")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("Do you really ")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("want to change?")


def changeNameMSSV():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("CHANGE INFO:Connect")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("to MIS-CTU wifi & ")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("open browser to")
    LCD.setCursor(0, 3)  # row, column
    my_ip = subpro.check_output(["hostname", "-I"]).decode("utf-8")[:-2]+":7497"
    LCD.write(my_ip) # get current ip address


# ------------------------------ Admin level interfaces ------------------------------
def mainAdminPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("ADMIN MENU:")
    LCD.setCursor(2, 1)  # row, column
    LCD.write("1. Info Locker")  # show info of all lockers to admin
    LCD.setCursor(2, 2)  # row, column
    LCD.write("2. Modify Database")  # instruction on how to modify the database
    LCD.setCursor(2, 3)  # row, column
    LCD.write("3. Delete Database")  # delete all the database


def warningDeletePage():
    LCD.setCursor(6, 0)  # row, column
    LCD.write("CAUTION")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Do this will delete")
    LCD.setCursor(0, 2)  # row, column
    LCD.write("all database (system")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("and fingerprint).Ok?")


def DBdeleteDonePage():
    LCD.setCursor(2, 2)  # row, column
    LCD.write("DATABASE DELETED!")


def modifyDatabaseInfoPage():
    LCD.setCursor(0, 0)  # row, column
    LCD.write("Connect to SSH with:")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("MISlocker@")
    LCD.setCursor(0, 2)  # row, column
    LCD.write(subpro.check_output(["hostname", "-I"]).decode("utf-8")[:-2])
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Pass: raspberry")


def infoLockerPage(name, mssv, current_locker):
    LCD.setCursor(4, 0)  # row, column
    LCD.write("INFO LOCKER " + str(current_locker))
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Name: " + name)
    LCD.setCursor(0, 2)  # row, column
    LCD.write("MSSV: " + mssv)
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Unlock?")


def infoLockerTempPage(current_locker):
    LCD.setCursor(4, 0)  # row, column
    LCD.write("INFO LOCKER " + str(current_locker))
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Temporary User")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("Unlock?")


def infoLockerNoInfoPage(current_locker):
    LCD.setCursor(4, 0)  # row, column
    LCD.write("INFO LOCKER " + str(current_locker))
    LCD.setCursor(0, 2)  # row, column
    LCD.write("No available")
    LCD.setCursor(0, 3)  # row, column
    LCD.write("information")


def unlockConfirmPage(locker_num):
    LCD.setCursor(0, 0)  # row, column
    LCD.write("UNLOCKED!")
    LCD.setCursor(0, 1)  # row, column
    LCD.write("Locker: " + str(locker_num))
    LCD.setCursor(0, 3)  # row, column
    LCD.write("User deleted!")
