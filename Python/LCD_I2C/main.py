import lcd
import time


def main():  # Main program block
    lcd.begin()
    time.sleep(5)
    lcd.clear()
    lcd.waitPage()
    time.sleep(5)
    lcd.clear()
    lcd.welcomePage('Dao Minh An', 'B1509360', str(5))


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
