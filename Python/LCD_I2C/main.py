
from builtins import KeyboardInterrupt
from LCD_I2C import LCD_I2C

# ---------------------------- Private Constant:
# -----Address and Screen parameter:
LCD_ADDRESS = 0x27
LCD_WIDTH   = 20
LCD_HEIGHT  = 4


def main(): # Main program block
    lcd = LCD_I2C(LCD_ADDRESS,LCD_WIDTH,LCD_HEIGHT)

    lcd.init()
    lcd.backlight()
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.write("SYSTEM STARTING")
    lcd.setCursor(7, 1)
    lcd.write("...")
    lcd.setCursor(3, 2)
    lcd.write("SYSTEM STARTING")
    lcd.setCursor(7, 3)
    lcd.write("...")


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass