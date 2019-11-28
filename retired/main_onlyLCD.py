import lcd
import time


def main():  # Main program block
    lcd.begin()

    time.sleep(3)

    lcd.clear()
    lcd.infoLockerTempPage()

    time.sleep(3)

    lcd.clear()
    lcd.welcomeTempPage(3)

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
    lcd.pointerPos(3, 1)

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

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.waitPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.unknownIDPage()
    lcd.pointerPos(2, 2)

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addFingerPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addFingerSuccessPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addFingerFailPage()
    lcd.pointerPos(2, 1)

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addRFIDPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addRFIDSuccessPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addRFIDFailPage()
    lcd.pointerPos(2, 1)

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.addExtraInfoPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.welcomePage('Dao Minh An', 'B1509360', 7)

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.returnPage('Dao Minh An', 7)

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.questionPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.continueUsingPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.mainAdminPage()
    lcd.pointerPos(2, 1)

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.modifyDatabaseInfoPage()

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.infoLockerPage('Dao Minh An', 'B1509360')

    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(button.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)
    print(switches.read())
    time.sleep(0.5)

    lcd.clear()
    lcd.unlockConfirmPage(3)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
