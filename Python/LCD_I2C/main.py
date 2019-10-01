from builtins import KeyboardInterrupt
from LCD import LCD
import time

# ---------------------------- Private Constant:
# -----Address and Screen parameter:
LCD_ADDRESS = 0x27
LCD_WIDTH = 20
LCD_HEIGHT = 4


def main():  # Main program block
    lcd = LCD(LCD_ADDRESS, LCD_WIDTH, LCD_HEIGHT)
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
