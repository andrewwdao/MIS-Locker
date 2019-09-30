"""------------------------------------------------------------*-
  LCD application module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Can Tho University 2019
  version 1.00 - 02/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import LCD_I2C


class LCD(LCD_I2C):
    # ---------------------------- Private Parameters:
    # -----Address and Screen parameter:

    # ------------------------------ Basic functions ------------------------------
    def __init__(self, lcd_addr, lcd_cols, lcd_rows, lcd_backlight, char_size):
        super().__init__(lcd_addr, lcd_cols, lcd_rows, lcd_backlight, char_size)
        self.begin()
        self.backlight()
        self.clear()
        self.setCursor(2, 1)  # row, column
        self.write("SYSTEM  STARTING")
        self.setCursor(7, 2)  # row, column
        self.write("...")

    def pointerPos(self, options, pointer):
        for pos in range(options):
            if pos == pointer:
                self.setCursor(0, pos)  # row, column
                self.write(">")
            else:
                self.setCursor(0, pos)  # row, column
                self.write(" ")

    # ------------------------------ User level interfaces ------------------------------
    def waitPage(self):  # user can use RFID or their fingerprint
        self.setCursor(4, 1)  # row, column
        self.write("SYSTEM READY")
        self.setCursor(5, 2)  # row, column
        self.write("waiting...")

    def welcomePage(self, name, mssv, locker_num):
        self.setCursor(6, 0)  # row, column
        self.write("WELCOME TO MIS!")
        self.setCursor(0, 1)  # row, column
        self.write("Name: " + name)
        self.setCursor(0, 2)  # row, column
        self.write("MSSV: " + mssv)
        self.setCursor(0, 3)  # row, column
        self.write("Your Locker is " + locker_num)

    def addExtraInfoPage(self, name, mssv):
        self.setCursor(0, 0)  # row, column
        self.write("Name: " + name)
        self.setCursor(0, 1)  # row, column
        self.write("MSSV: " + mssv)
        self.setCursor(2, 2)  # row, column
        self.write("New RFID")
        self.setCursor(2, 3)  # row, column
        self.write("New fingerprint")

    def welcomePageTemp(self, locker_num):
        self.setCursor(3, 0)  # row, column
        self.write("TEMPORARY USER")
        self.setCursor(0, 1)  # row, column
        self.write("This is a one-time")
        self.setCursor(0, 2)  # row, column
        self.write("user only.")
        self.setCursor(0, 3)  # row, column
        self.write("Your Locker is " + locker_num)

    def unknownIDPage(self):
        self.setCursor(1, 0)  # row, column
        self.write("NOT RECOGNISED ID!")
        self.setCursor(2, 2)  # row, column
        self.write("Add New ID")
        self.setCursor(2, 3)  # row, column
        self.write("Add Existed ID")

    def addFingerPage(self, number):
        self.setCursor(2, 0)  # row, column
        self.write("ADD  FINGERPRINT")
        self.setCursor(2, 2)  # row, column
        self.write("Put your finger")
        self.setCursor(2, 3)  # row, column
        self.write("in position " + number)

    def addFingerPageSuccess(self):
        self.setCursor(2, 0)  # row, column
        self.write("ADD  FINGERPRINT")
        self.setCursor(1, 1)  # row, column
        self.write("Fingerprint added!")
        self.setCursor(0, 3)  # row, column
        self.write("Press any to return")

    def addFingerPageFail(self):
        self.setCursor(2, 0)  # row, column
        self.write("ADD  FINGERPRINT")
        self.setCursor(6, 1)  # row, column
        self.write("Failed!")
        self.setCursor(2, 2)  # row, column
        self.write("Retry")
        self.setCursor(2, 3)  # row, column
        self.write("Cancel")

    def addRFIDPage(self):
        self.setCursor(6, 0)  # row, column
        self.write("ADD RFID")
        self.setCursor(2, 1)  # row, column
        self.write("Put your RFID")
        self.setCursor(2, 2)  # row, column
        self.write("in the reader")

    def addRFIDPageSuccess(self):
        self.setCursor(6, 0)  # row, column
        self.write("ADD RFID")
        self.setCursor(4, 1)  # row, column
        self.write("RFID added!")
        self.setCursor(0, 3)  # row, column
        self.write("Press any to return")

    def addRFIDPageFail(self):
        self.setCursor(6, 0)  # row, column
        self.write("ADD RFID")
        self.setCursor(6, 1)  # row, column
        self.write("Failed!")
        self.setCursor(2, 2)  # row, column
        self.write("Retry")
        self.setCursor(2, 3)  # row, column
        self.write("Cancel")

    def addInfoPage(self):
        self.setCursor(5, 0)  # row, column
        self.write("ADD NEW INFO")
        self.setCursor(0, 1)  # row, column
        self.write("Connect to MIS-CTU")
        self.setCursor(0, 2)  # row, column
        self.write("wifi & open browser")
        self.setCursor(0, 3)  # row, column
        self.write("to: mis-locker.ctu")

    # ------------------------------ Admin level interfaces ------------------------------
    def mainPageDatabase(self):
        self.setCursor(0, 0)  # row, column
        self.write("ADMIN MENU:")
        self.setCursor(2, 1)  # row, column
        self.write("1. Export Database")  # export will export everything
        self.setCursor(2, 2)  # row, column
        self.write("2. Import Database")  # import will have 2 options: append and override
        self.setCursor(2, 3)  # row, column
        self.write("3. Clear Database")  #

    def exportSuccess(self):
        self.setCursor(2, 0)  # row, column
        self.write("EXPORT DATABASE")
        self.setCursor(7, 1)  # row, column
        self.write("Done!")
        self.setCursor(0, 3)  # row, column
        self.write("Press any to return")

    def exportFail(self):
        self.setCursor(2, 0)  # row, column
        self.write("EXPORT DATABASE")
        self.setCursor(6, 1)  # row, column
        self.write("Failed!")
        self.setCursor(2, 2)  # row, column
        self.write("Retry")
        self.setCursor(2, 3)  # row, column
        self.write("Cancel")

    def importPage(self):
        self.setCursor(2, 0)  # row, column
        self.write("IMPORT DATABASE")
        self.setCursor(2, 2)  # row, column
        self.write("1. Append database")
        self.setCursor(2, 3)  # row, column
        self.write("2. New database")

    def importSuccess(self):
        self.setCursor(2, 0)  # row, column
        self.write("IMPORT DATABASE")
        self.setCursor(7, 1)  # row, column
        self.write("Done!")
        self.setCursor(0, 3)  # row, column
        self.write("Press any to return")

    def importFail(self):
        self.setCursor(2, 0)  # row, column
        self.write("IMPORT DATABASE")
        self.setCursor(6, 1)  # row, column
        self.write("Failed!")
        self.setCursor(2, 2)  # row, column
        self.write("Retry")
        self.setCursor(2, 3)  # row, column
        self.write("Cancel")

    def mainPageLocker(self):
        self.setCursor(0, 0)  # row, column
        self.write("ADMIN MENU:")
        self.setCursor(2, 1)  # row, column
        self.write("4. Check Info Locker")  # check any locker that has information in

    def infoLocker(self, name, mssv):
        self.setCursor(4, 0)  # row, column
        self.write("INFO LOCKER")
        self.setCursor(0, 1)  # row, column
        self.write("Name: " + name)
        self.setCursor(0, 2)  # row, column
        self.write("MSSV: " + mssv)
        self.setCursor(2, 3)  # row, column
        self.write("Unlock?")

    def infoLockerTemp(self):
        self.setCursor(4, 0)  # row, column
        self.write("INFO LOCKER")
        self.setCursor(0, 1)  # row, column
        self.write("Temporary User")
        self.setCursor(2, 3)  # row, column
        self.write("Unlock?")