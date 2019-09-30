"""------------------------------------------------------------*-
  LCD I2C python module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Can Tho University 2019
  version 1.00 - 01/10/2019
 --------------------------------------------------------------
 * Credited tutorials and Libraries:
 * - Drive i2c LCD Screen with Raspberry Pi:
    http://osoyoo.com/?p=1031
 * - LiquidCrystal_I2C library for Arduino:
    https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library
 --------------------------------------------------------------"""
import smbus
import time


class LCD_I2C:
    # ---------------------------- Private Parameters:
    # -----Address and Screen parameter:
    _Addr = int()
    _cols = int()
    _rows = int()
    _chsize = int()
    _backlightval = int()
    _displayfunction = int()
    _displaycontrol = int()
    _displaymode = int()
    LCD_LINE1 = 0x80  # LCD RAM address for the 1st line (0x80|0x00)
    LCD_LINE2 = 0xC0  # LCD RAM address for the 2nd line (0x80|0x40)
    LCD_LINE3 = 0x94  # LCD RAM address for the 3rd line (0x80|0x14)
    LCD_LINE4 = 0xD4  # LCD RAM address for the 4th line (0x80|0x54)
    # -----Command:
    LCD_DAT = 1  # Mode - Sending data
    LCD_CMD = 0  # Mode - Sending command
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    # LCD_SETCGRAMADDR    = 0x40
    # LCD_SETDDRAMADDR    = 0x80
    # -----Important Bits:
    En = 0b00000100  # Enable bit
    # Rw = 0b00000010  # Read/Write bit
    # Rs = 0b00000001  # Register select bit
    # -----Function Flags:
    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00
    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00
    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_1LINE = 0x00
    LCD_LINES = 0x08
    LCD_5X10DOTS = 0x04
    LCD_5X8DOTS = 0x00
    # flags for Back light:
    LCD_BACKLIGHT = 0x08  # On
    LCD_NOBACKLIGHT = 0x00  # Off
    # -----Timing constants:
    PULSE = 0.000001  # 1us - Enable pulse must be >450ns
    DELAY = 0.0005  # 5ms
    WAIT = 0.002  # 2ms
    # -----Open I2C interface:
    # bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
    bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

    def __init__(self, lcd_addr=0x27, lcd_cols=20, lcd_rows=4, lcd_backlight=LCD_NOBACKLIGHT, char_size=LCD_5X8DOTS):
        self._Addr = lcd_addr
        self._cols = lcd_cols
        self._rows = lcd_rows
        self._chsize = char_size
        self._backlightval = lcd_backlight
        self._displayfunction = 0x00
        self._displaycontrol = 0x00
        self._displaymode = 0x00

    def begin(self):
        self.bus = smbus.SMBus(1)  # Rev 2 Pi uses 1
        '''
        SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
	    according to datasheet, we need at least 40ms after power rises above 2.7V
	    before sending commands. Raspberry Pi can turn on way better 4.5V so we'll wait 50ms
        '''
        time.sleep(self.DELAY * 100)  # 50ms

        # Now we pull both RS and R/W low to begin commands
        self.writeByte(self._backlightval)  # // reset expander and turn backlight off (Bit 8 =1)
        time.sleep(1)

        '''
        put the LCD into 4 bit mode
	    this is according to the hitachi HD44780 datasheet. Figure 24, pg 46
	    we start in 8bit mode, try to set 4 bit mode
        '''
        self.command(0x33)  # 110011 Initialise to become 4bit mode
        self.command(0x32)  # 110010 Initialise to become 4bit mode

        # Data length, number of lines, font size, etc
        self._displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5X8DOTS

        if self._rows > 1:
            self._displayfunction |= self.LCD_LINES

        # for some 1 line displays you can select a 10 pixel high font
        if (self._chsize != self.LCD_5X8DOTS) & (self._rows == 1):
            self._displayfunction |= self.LCD_5X10DOTS

        # Send these information to the LCD
        self.command(self.LCD_FUNCTIONSET | self._displayfunction)

        # turn the display on with no cursor or blinking default (Display On,Cursor Off, Blink Off)
        self._displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.display()

        # clear it off
        self.clear()

        # Initialize to default text direction (for roman languages)
        self._displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.command(self.LCD_ENTRYMODESET | self._displaymode)

        # Start from home:
        self.command(self.LCD_RETURNHOME)
        time.sleep(self.WAIT)

    # ------------------------------ Command for Users ------------------------------
    def noBacklight(self):  # Turn the (optional) backlight off/on
        self._backlightval = self.LCD_NOBACKLIGHT
        self.writeByte(0)

    def backlight(self):
        self._backlightval = self.LCD_BACKLIGHT
        self.writeByte(0)

    def clear(self):
        self.command(self.LCD_CLEARDISPLAY)  # clear display, set cursor position to zero
        time.sleep(self.WAIT)

    def setCursor(self, col, row):
        row_offsets = (self.LCD_LINE1, self.LCD_LINE2, self.LCD_LINE3, self.LCD_LINE4)  # tuple
        if row > self._rows:
            row = self._rows - 1  # we count rows starting w / 0
        self.command(col + row_offsets[row])

    def display(self):
        self._displaycontrol |= self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL | self._displaycontrol)

    def noDisplay(self):
        self._displaycontrol &= ~self.LCD_DISPLAYON
        self.command(self.LCD_DISPLAYCONTROL | self._displaycontrol)

    # ------------------------------ Mid level commands ------------------------------
    def command(self, _value):
        self.send(_value, self.LCD_CMD)

    def write(self, _string):
        for i in range(len(_string)):
            self.send(ord(_string[i]), self.LCD_DAT)

    # ------------------------------ Low level data sending Commands ------------------------------
    def send(self, _data, _mode):  # write either command or data
        high_bits = _data & 0xF0
        low_bits = (_data << 4) & 0xF0
        self.write4bits(high_bits | _mode)
        self.write4bits(low_bits | _mode)

    def write4bits(self, _data):
        self.writeByte(_data)
        self.pulseEnable(_data)

    def writeByte(self, _data):  # Compressor for bus write_byte
        self.bus.write_byte(self._Addr, (_data | self._backlightval))

    def pulseEnable(self, _data):  # Toggle enable
        self.writeByte(_data | self.En)  # Enable High
        time.sleep(self.PULSE)  # Enable pulse must be >450ns
        self.writeByte(_data & ~self.En)  # Enable Low
        time.sleep(self.DELAY)  # commands need > 37us to settle
