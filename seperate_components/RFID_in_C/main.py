"""*------------------------------------------------------------*-
  Wiegand Reader - python main file
  Tested with Gwiot 7304D2 RFID Reader(26 bit Wiegand mode) and RASPBERRY PI 3B+
    (c) Minh-An Dao 2019
    (c) Spiros Ioannou 2017
  version 1.10 - 25/10/2019
 --------------------------------------------------------------
 * RFID reader using Wiegand 26 protocol.
 * Use both 125Khz and 315Mhz Cards
 *
 *  ------ Pinout ------
 *  1(RED)    - VCC     - DC 9-12V
 *  2(BROWN)  - FORMAT  - Keep floating to use wiegand26, connect to GND to use weigang34
 *  3(BLUE)   - OUT     - 5V in normal condition, GND when card was scanned
 *  4(YELLOW) - Buzzer  - pull up automatically (5V), pull to GND to make it beep.
 *  5(ORANGE) - LED     - pull up automatically (5V) - RED, pull to GND to make it GREEN.
 *  6(GREEN)  - DATA0   - Wiegand DATA0 pin.
 *  7(WHITE)  - DATA1   - Wiegand DATA1 pin.
 *  8(BLACK)  - GND
 *
 --------------------------------------------------------------"""
import rfid
import time
try:
    rfid.start()
    time.sleep(1)
    while True:
        [rfid_status, rfid_tag] = rfid.check()
        print(rfid_status)
        print(rfid_tag)
        print('hope this works')
        time.sleep(1)
except KeyboardInterrupt:
    rfid.stop() # REMEMBER TO DO THIS SINCE THE READING IN C DON'T EXIT BY ITSELF!
    pass

