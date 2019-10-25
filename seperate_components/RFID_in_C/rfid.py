"""*------------------------------------------------------------*-
  Weigang Reader - Gwiot 7304D2 - header file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  (c) Spiros Ioannou 2017
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
 * This is interrupt drivern, no polling occurs.
 * After each bit is read, a timeout is set.
 * If timeout is reached read code is evaluated for correctness.
 *
 * Wiegand Bits:
 * pFFFFFFFFNNNNNNNNNNNNNNNNP
 * p: even parity of F-bits and leftmost 4 N-bits
 * F: Facility code
 * N: Card Number
 * P: odd parity of rightmost 12 N-bits
 --------------------------------------------------------------"""
import subprocess
import sys

TARGET = './wiegand_rpi'

p = subprocess.Popen([TARGET], shell=False, stdout=subprocess.PIPE)
print('ready!')
while True:
    # print ("Looping")
    line = p.stdout.readline()
    print(str(line.strip()))
    if line.strip() == b'done!':
        print("success!")
        sys.stdout.flush()
        exit()
    sys.stdout.flush()
