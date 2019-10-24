"""*------------------------------------------------------------*-
  Weigang Reader - Gwiot 7304D2 - header file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  (c) Alperen Güman 2017
  version 1.00 - 24/10/2019
 --------------------------------------------------------------
 * RFID reader using Weigang 26 protocol.
 * Use both 125Khz and 315Mhz Cards
 *  
 *  ------ Pinout ------
 *  1(RED)    - VCC     - DC 9-12V
 *  2(BROWN)  - FORMAT  - Keep floating to use weigang26, connect to GND to use weigang34
 *  3(BLUE)   - OUT     - 5V in normal condition, GND when card was scanned
 *  4(YELLOW) - Buzzer  - pull up automatically (5V), pull to GND to make it beep.
 *  5(ORANGE) - LED     - pull up automatically (5V) - RED, pull to GND to make it GREEN.
 *  6(GREEN)  - DATA0   - Weigang DATA0 pin.
 *  7(WHITE)  - DATA1   - Weigang DATA1 pin.
 *  8(BLACK)  - GND
 * 
 --------------------------------------------------------------"""
import RPi.GPIO as GPIO  # default as BCM mode!
import time

# ---------------------------- Configurable parameters -------------------------
# -----Pin connection:
DATA_0 = 21  # GPIO BCM Pin 21 | Green cable | Data0
DATA_1 = 20  # GPIO BCM Pin 20 | White cable | Data1
BUZZER = 16  # GPIO BCM Pin 16 | Yellow cable | Sound

# -----Weigang parameters:
MAX_WG_BITS = 32
READER_TIMEOUT = 3000000  # ns
WG_LEN = 256
DEBOUNCE = 10
FAST_INTERVAL = 0.5


class Gwiot_7304D2:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(DATA_0, GPIO.IN)  # auto pull up already by the weigang
        GPIO.setup(DATA_1, GPIO.IN)  # auto pull up already by the weigang
        GPIO.setup(BUZZER, GPIO.OUT)  # only a signal pin, not a power pin!
        GPIO.output(BUZZER, GPIO.HIGH)  # Buzzer OFF

        self.__wiegandData = bytearray(MAX_WG_BITS)  # a limited list of bytes
        self.__wiegandBitCount = 0
        self.__wiegand_s = time.time()  # time since epoch in second
        self.__wiegand_us = time.time_ns()  # time since epoch in nano second

        GPIO.add_event_detect(DATA_0, GPIO.FALLING, callback=self.getData0_ISR, bouncetime=DEBOUNCE)
        GPIO.add_event_detect(DATA_1, GPIO.FALLING, callback=self.getData1_ISR, bouncetime=DEBOUNCE)

    def getData0_ISR(self,channel):
        if (self.__wiegandBitCount / 8) < MAX_WG_BITS:
            self.__wiegandData[int(self.__wiegandBitCount / 8)] <<= 1  # add 0 to the byte
            self.__wiegandBitCount += 1
        self.__wiegand_s = time.time()  # time since epoch in second
        self.__wiegand_us = time.time_ns()  # time since epoch in nano second

    def getData1_ISR(self,channel):
        if (self.__wiegandBitCount / 8) < MAX_WG_BITS:
            self.__wiegandData[int(self.__wiegandBitCount / 8)] <<= 1  # add 1 to the byte
            self.__wiegandData[int(self.__wiegandBitCount / 8)] |= 1
            self.__wiegandBitCount += 1
        self.__wiegand_s = time.time()  # time since epoch in second
        self.__wiegand_us = time.time_ns()  # time since epoch in nano second

    def reset(self):
        self.__wiegandData = bytearray(MAX_WG_BITS)  # a limited list of bytes
        self.__wiegandBitCount = 0

    def getPendingBitCount(self):
        temp_s = time.time() - self.__wiegand_s
        temp_us = time.time_ns() - self.__wiegand_us
        if (temp_s > 1) | (temp_us > READER_TIMEOUT):
            return self.__wiegandBitCount
        return 0

    def lengthByte(self):
        return self.__wiegandBitCount / 8 + 1

    def available(self):
        if self.getPendingBitCount() > 0:
            return True
        return False

    def readData(self):
        data = self.__wiegandData.decode('utf-8')
        self.reset()
        return data

    def buzzer(self):
        GPIO.output(BUZZER, GPIO.LOW)  # Buzzer ON
        time.sleep(FAST_INTERVAL)
        GPIO.output(BUZZER, GPIO.HIGH)  # Buzzer OFF
        time.sleep(FAST_INTERVAL)
