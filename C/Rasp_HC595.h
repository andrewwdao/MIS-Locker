/*------------------------------------------------------------*-
  HC595 Controller - header file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  version 1.00 - 02/10/2019
 --------------------------------------------------------------
 * TRANSFERING DATA FROM SERIAL TO PARALLEL USING SPI PROTOCOL AND IC 74HC595
 *  
 *  ------74HC595
 *  1 - QB      16 - VCC
 *  2 - QC      15 - QA
 *  3 - QD      14 - SER    - connect to DS_PIN - DATA_PIN  or to QH' of the previous 74HC595
 *  4 - QE      13 - !OE    - connect to GND  
 *  5 - QF      12 - RCLK   - connect to STCP_PIN - LATCH_PIN (even when get data from a 74HC595 not a MCU)
 *  6 - QG      11 - SRCLK  - connect to SHCP_PIN - CLOCK_PIN (even when get data from a 74HC595 not a MCU)
 *  7 - QH      10 - !SRCLR - connect to VCC
 *  8 - GND     9  - QH'    - left floated when using only 1 74HC595, connect to pin 14 (SER) of the next 74HC595 if using multiple ones.
 * 
 -------------------------------------------------------------- */
#ifndef __RASP_HC595_H
#define __RASP_HC595_H
#include <stdio.h>
//#include <stdlib.h>     /* atof */
#include <wiringPi.h>
#include <wiringShift.h>

// ------ Public constants ------------------------------------

// ------ Public function prototypes --------------------------
/**
Initialize BOTH HC595 modules for 20 lockers
*/
void HC595s_init();
/**
Send data for the first HC595 module
*/
void HC595a_send(char, char, char);
/**
Send data for the second HC595 module
*/
void HC595b_send(char, char, char);
// ------ Public variable -------------------------------------

#endif // __RASP_HC595_H
