/*------------------------------------------------------------*-
  Wiegand Reader - header file
  Tested with Gwiot 7304D2 RFID Reader(26 bit Wiegand mode) and RASPBERRY PI 3B+
  (c) Spiros Ioannou 2017
  (c) Minh-An Dao 2019
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
 -------------------------------------------------------------- */
#ifndef __RFID_WIEGAND_H
#define __RFID_WIEGAND_H
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <memory.h>
#include <stdint.h>
#include <sys/time.h>
#include <signal.h>
#include <wiringPi.h>

// ------ Public constants ------------------------------------

// ------ Public function prototypes --------------------------
/**
Initialize the whole rfid system including GPIOs, interrupts and handlers
*/
void rfid_init(int, int, int, int);
/**
Show usage information for the user
*/
void rfid_showUsage();
// ------ Public variable -------------------------------------

#endif //__RFID_WIEGAND_H