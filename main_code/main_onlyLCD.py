import lcd
import time


def main():  # Main program block
    lcd.begin()

    time.sleep(3)

    lcd.clear()
    lcd.waitPage()

    time.sleep(3)

    lcd.clear()
    lcd.addExtraInfoPage('Dao Minh An', 'B1509360')
    lcd.pointerPos(2, 1)

    time.sleep(3)

    lcd.clear()
    lcd.unknownIDPage()
    lcd.pointerPos(2, 1)

    time.sleep(3)

    lcd.clear()
    lcd.addFingerPage()

    time.sleep(3)

    lcd.clear()
    lcd.addFingerSuccessPage()

    time.sleep(3)

    lcd.clear()
    lcd.addFingerFailPage()
    lcd.pointerPos(2, 1)

    time.sleep(3)

    lcd.clear()
    lcd.addRFIDPage()

    time.sleep(3)

    lcd.clear()
    lcd.addRFIDSuccessPage()

    time.sleep(3)

    lcd.clear()
    lcd.addRFIDFailPage()
    lcd.pointerPos(2, 1)

    time.sleep(3)

    lcd.clear()
    lcd.addInfoPage()

    time.sleep(3)

    lcd.clear()
    lcd.welcomePage('Dao Minh An', 'B1509360', 7)

    time.sleep(3)

    lcd.clear()
    lcd.returnPage('Dao Minh An', 7)

    time.sleep(3)

    lcd.clear()
    lcd.questionPage()
    lcd.pointerPos(2, 2)

    time.sleep(3)

    lcd.clear()
    lcd.continueUsingPage()

    time.sleep(3)

    lcd.clear()
    lcd.mainAdminPage()
    lcd.pointerPos(3, 1)

    time.sleep(3)

    lcd.clear()
    lcd.modifyDatabaseInfoPage()

    time.sleep(3)

    lcd.clear()
    lcd.infoLockerPage('Dao Minh An', 'B1509360')

    time.sleep(3)

    lcd.clear()
    lcd.unlockConfirmPage(3)




if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
