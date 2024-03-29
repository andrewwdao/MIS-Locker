# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyRfid
Copyright (C) 2015 Philipp Meisberger <team@pm-codeworks.de>
Copyright (C) 2019 Minh-An Dao <minhan7497@gmail.com>

All rights reserved.

"""

import serial
import os
import struct
import RPi.GPIO as GPIO  # default as BCM mode!

READY = False
BUFFER_SIZE = 14
CHECKSUM_SIZE = 2
DATA_SIZE = 10
RF_DEBOUNCE = 1  # second

def ISR(channel):
    global READY
    READY = True


class PyRfid(object):
    """
    A python written library for an 125kHz RFID reader using the EM4100 protocol.

    Flag for RFID connection start.
    @var hex RFID_STARTCODE

    Flag for RFID connection end.
    @var hex RFID_ENDCODE

    UART serial connection via PySerial.
    @var Serial __serial

    Holds the complete tag after reading.
    @var string __rawTag
    """

    INT_PIN = 22  # BCM GPIO 22 - wiringPi 3
    DEBOUNCE = 700
    RFID_STARTCODE = 0x02
    RFID_ENDCODE = 0x03
    __serial = None
    __rawTag = None

    def __init__(self, port='/dev/ttyUSB0', baudRate=9600):
        """
        Constructor

        @param  port string
        @param baudRate integer
        """

        # Validates port
        if not os.path.exists(port):
            raise Exception('The RFID sensor port "' + port + '" was not found!')

        # Initializes connection
        self.__serial = serial.Serial(port=port, baudrate=baudRate, bytesize=serial.EIGHTBITS, timeout=1)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.INT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.INT_PIN, GPIO.RISING, callback=ISR, bouncetime=self.DEBOUNCE)
        global READY
        READY = False

    def __del__(self):
        """
        Destructor

        """

        # Closes connection if established
        if (self.__serial is not None) and (self.__serial.isOpen()):
            self.__serial.close()

    def __read(self):
        """
        Reads the complete tag and returns status.

        @return boolean
        """
        global READY

        self.__rawTag = None
        rawTag = ''
        calculatedChecksum = 0
        receivedPacketData = []
        index = 0

        count = 0
        # buffer with 14 chars
        buffer = [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
        buffer_index = 0
        while READY:

            # Reads on byte
            receivedFragment = self.__serial.read()

            # Collects RFID data
            if len(receivedFragment) != 0:

                if receivedFragment == self.RFID_STARTCODE:
                    count = 0
                    buffer_index = 1
                    rawTag += receivedFragment  # everything is alright => copy first letter into buffer
                    while True:
                        receivedFragment = self.__serial.read()
                        buffer_index += 1
                        rawTag += receivedFragment  # everything is alright => copy current value to buffer
                        if receivedFragment == self.RFID_ENDCODE:
                            if buffer_index == BUFFER_SIZE:
                                print(rawTag)
                                READY = False
                                return True
                            else:
                                print('error')

                # Sets complete tag for other methods
                self.__rawTag = rawTag



    # def __read(self):
    #     """
    #     Reads the complete tag and returns status.
    #
    #     @return boolean
    #     """
    #     global READY
    #
    #     self.__rawTag = None
    #     rawTag = ''
    #     calculatedChecksum = 0
    #     receivedPacketData = []
    #     index = 0
    #
    #     while READY:
    #
    #         # Reads on byte
    #         receivedFragment = self.__serial.read()
    #
    #         # Collects RFID data
    #         if len(receivedFragment) != 0:
    #
    #             # Start and stop bytes are string encoded and must be byte encoded
    #             if (index == 0) or (index == 13):
    #                 receivedFragment = struct.unpack('@B', receivedFragment)[0]
    #             else:
    #                 rawTag += str(struct.unpack('@B', receivedFragment)[0])
    #                 receivedFragment = int(receivedFragment, 16)
    #
    #             # Collects RFID data (hexadecimal)
    #             receivedPacketData.append(receivedFragment)
    #             index += 1
    #
    #         # Packet completely received
    #         if index == 14:
    #
    #             # Checks for invalid packet data
    #             if (receivedPacketData[0] != self.RFID_STARTCODE) or (receivedPacketData[13] != self.RFID_ENDCODE):
    #                 raise Exception('Invalid start or stop bytes!')
    #
    #             # Calculates packet checksum
    #             for i in range(1, 11, 2):
    #                 byte = receivedPacketData[i] << 4
    #                 byte = byte | receivedPacketData[i + 1]
    #                 calculatedChecksum = calculatedChecksum ^ byte
    #
    #             # Gets received packet checksum
    #             receivedChecksum = receivedPacketData[11] << 4
    #             receivedChecksum = receivedChecksum | receivedPacketData[12]
    #
    #             # Checks for wrong checksum
    #             if calculatedChecksum != receivedChecksum:
    #                 raise Exception('Calculated checksum is wrong!')
    #
    #             # Sets complete tag for other methods
    #             self.__rawTag = rawTag
    #
    #             READY = False
    #             return True

    def readTag(self):
        """
        Reads the complete raw tag.

        @return boolean
        """

        try:
            if self.__read():
                return True
            else:
                return False

        except KeyboardInterrupt:
            return False

    @property
    def rawTag(self):
        """
        Returns read raw tag in hexadecimal format "1A2B345C67" without checksum.

        @return string (10 bytes)
        """

        return self.__rawTag[0:10]

    @property
    def tagType(self):
        """
        Returns type of read tag (first 4 bytes).

        @return hex (4 bytes)
        """

        if self.__rawTag is not None:
            return hex(int(self.__rawTag[0:4], 16))

        return None

    @property
    def tagTypeFloat(self):
        """
        Returns type of read tag (first 2 bytes).

        @return hex (2 bytes)
        """

        if self.__rawTag is not None:
            return hex(int(self.__rawTag[0:2], 16))

        return None

    @property
    def tagId(self):
        """
        Returns ID of read tag in decimal format "0001234567".

        @return string (10 chars)
        """

        if self.__rawTag is not None:
            # Length of ID is 10 anyway
            return '%010i' % int(self.__rawTag[4:10], 16)

        return None

    @property
    def tagIdFloat(self):
        """
        Returns ID of read tag in float format "123,45678".

        @return string (9 chars)
        """

        if self.__rawTag is not None:
            pre = float.fromhex(self.__rawTag[2:6])
            post = float.fromhex(self.__rawTag[6:10]) / 100000
            tag = pre + post
            return str(tag)

        return None

    @property
    def tagChecksum(self):
        """
        Returns checksum of read tag (last 2 bytes).

        @return hex (2 bytes)
        """

        if self.__rawTag is not None:
            return hex(int(self.__rawTag[10:12], 16))

        return None
