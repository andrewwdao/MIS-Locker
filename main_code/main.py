import lcd
from adc import adc_button, adc_switches
import time

button = adc_button()
switches = adc_switches()


def main():  # Main program block
    lcd.begin()
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
    lcd.addFingerPage(1)

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


# lcd.addInfoPage()
#    lcd.addExtraInfoPage('Dao Minh An', 'B1509360')
#    lcd.pointerPos(2, 1)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
