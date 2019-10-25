"""*------------------------------------------------------------*-
  Wiegand Reader - python module file
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
 * This is interrupt driven, no polling occurs.
 * After each bit is read, a timeout is set.
 * If timeout is reached read code is evaluated for correctness.
 *
 * Wiegand Bits:
 * pFFFFFFFFNNNNNNNNNNNNNNNNP
 * p: even parity of F-bits and leftmost 4 N-bits
 * F: Facility code
 * N: Card Number
 * P: odd parity of rightmost 12 N-bits
 *
 * Usage:
 * ./rfid_main [-d] [-h] [-a] [-0 D0-pin] [-1 D1-pin]
 *  With:
 *  -d : debug mode
 *  -h : help
 *  -a : dumb all received information out
 *  -0 D0-pin: GPIO pin for data0 pulse (wiringPi pin)
 *  -1 D1-pin: GPIO pin for data1 pulse (wiringPi pin)
 *
 --------------------------------------------------------------"""
import subprocess as subpro
from ContinuousStreamRead import StreamReader
import sys

TARGET = './rfid_main'
rfid_object = object()
rfid_stream = object()

def start():
    global rfid_object, rfid_stream
    rfid_object = subpro.Popen([TARGET], shell=False, stdout=subpro.PIPE, stderr=subpro.PIPE)
    rfid_stream = StreamReader(rfid_object.stdout)
    print('RFID ready!')

def check():
    # while rfid_object.poll is None:
    # mes = rfid_object.communicate()[0]
    # err = ''
    # err = rfid_object.stderr.readline()
    # mes = rfid_object.stdout.readline()

    mes = rfid_stream.readline(0.1)
    err = ''

    # (mes, err) = rfid_object.communicate()
    sys.stdout.flush()
    sys.stderr.flush()
    return [str(mes.strip()),str(err.strip())]
    # line = p.stdout.readline()
    # print(str(line.strip()))
    # if line.strip() == b'done!':
    #     print("success!")
    #     sys.stdout.flush()
    #     exit()
    # sys.stdout.flush()

def stop():
    # check if process terminated or not
    if rfid_object.poll() is None:
        rfid_object.terminate()
        rfid_object.kill()
        print('RFID terminated!')

