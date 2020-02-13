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
import serial
from ContinuousStreamRead import StreamReader
import sys
import time

class Gwiot_7304D2:
    def __init__(self):
        self.TARGET = './rfid_main'
        self.rfid = subpro.Popen([self.TARGET], shell=False, stdout=subpro.PIPE, stderr=subpro.PIPE)
        self.mes = StreamReader(self.rfid.stdout)
        self.tag_id = ''
        print('RFID ready!')

    def hasID(self):
        mes = self.mes.readline(0.05)  # 0.05 secs to let the shell output the result
        sys.stdout.flush()
        if mes is not None:  # turn it into string if it is not a null
            self.tag_id = mes.strip().decode("utf-8")
            return True
        if mes is None or mes == 'CHECKSUM_FAILED':
            return False
    
    def flush(self):
        sys.stdout.flush() # flush all the left over from buffer
        return
    
    def tagID(self):
        return self.tag_id

    # def debugInfo(self):
    #     print('ID:       ' + self.tag_id)
    #     print('Nothing else to display here')

    def stop(self):
        # check if process terminated or not
        if self.rfid.poll() is None:
            self.rfid.terminate()
            self.rfid.kill()
            print('RFID terminated!')

# def start():
#     global rfid_object, rfid_mes
#     rfid_object = subpro.Popen([TARGET], shell=False, stdout=subpro.PIPE, stderr=subpro.PIPE)
#     rfid_mes = StreamReader(rfid_object.stdout)
#     print('RFID ready!')
#
#
# def check():
#     mes = rfid_mes.readline(0.05)  # 0.05 secs to let the shell output the result
#     sys.stdout.flush()
#     if mes is not None:  # turn it into string if it is not a null
#         mes = mes.strip().decode("utf-8")
#     if mes is None or mes == 'CHECKSUM_FAILED':
#         return [False, '']
#
#     return [True, mes]
#
#
# def stop():
#     # check if process terminated or not
#     if rfid_object.poll() is None:
#         rfid_object.terminate()
#         rfid_object.kill()
#         print('RFID terminated!')


############ DEPRECATED ###############


# sample key:
# ADMIN_KEY = '810093B8D6\r\n'

class RDM6300:
    # def __init__(self, port='/dev/ttyUSB0', baudRate=9600):
    def __init__(self, com_port='/dev/ttyUSB0', baud_rate=115200):
        # ----------------------------Class variable:
        self.__serial = serial.Serial(com_port, baudrate=baud_rate,
                                      parity=serial.PARITY_NONE,
                                      stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS,
                                      timeout = 1
                                      )
        if self.__serial.isOpen():
            self.__serial.close()

        self.__serial.open()

        self.__serial.flushInput()
        self.tag_id = ""
        time.sleep(1)
        print('RFID ready!')

    def hasID(self):
        try:
            line = self.__serial.readline().decode()
        except:
            line = ""
        if len(line):
            self.tag_id = line
            return True
        return False

    def flush(self):
        # dump buffer out, flush all the left over from buffer
        self.__serial.flushInput()

    def tagID(self):
        return self.tag_id

    # def debugInfo(self):
    #     print('RAW:      ' + self.rfid.rawTag)
    #     print('Checksum: ' + self.rfid.tagChecksum + '\n')
    #
    #     print('Decimal-format:')
    #     print('ID:       ' + self.rfid.tagId)
    #     print('Type:     ' + self.rfid.tagType + '\n')
    #
    #     print('Float-format:')
    #     print('ID:       ' + self.rfid.tagIdFloat)
    #     print('Type:     ' + self.rfid.tagTypeFloat)

    def stop(self):
        return
