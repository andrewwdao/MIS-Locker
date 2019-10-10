/*------------------------------------------------------------*-
  74HC595 Controller - function file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  version 1.30 - 10/10/2019
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
#ifndef  __RASP_HC595_CPP 
#define  __RASP_HC595_CPP
#include "Rasp_HC595.h"

// ------ Private constants -----------------------------------
//First HC595 module:
#define DS_PIN_a  	0 //Pin connected to SER - DATA PIN (or Pin14 - DS) of 74HC595 - pin 0 of wiringPi, GPIO17
#define STCP_PIN_a 	2 //Pin connected to RCLK - LATCH_PIN (or Pin12 - ST_CP) of 74HC595 - pin 2 of wiringPi, GPIO 27
#define SHCP_PIN_a 	3 //Pin connected to SRCLK - CLOCK_PIN (or Pin11 - SH_CP) of 74HC595 - pin 3 of wiringPi, GPIO 22
//Second HC595 module:
#define DS_PIN_b  	1 //Pin connected to SER - DATA PIN (or Pin14 - DS) of 74HC595 - pin 0 of wiringPi, GPIO17
#define STCP_PIN_b 	4 //Pin connected to RCLK - LATCH_PIN (or Pin12 - ST_CP) of 74HC595 - pin 2 of wiringPi, GPIO 27
#define SHCP_PIN_b 	5 //Pin connected to SRCLK - CLOCK_PIN (or Pin11 - SH_CP) of 74HC595 - pin 3 of wiringPi, GPIO 22

#define BEGIN_STATE 0b00000000
// ------ Private function prototypes -------------------------
/**
Slow down the original ShiftOut Function
*/
void myShiftOut(uint8_t,uint8_t,uint8_t,uint8_t);
/**
Send data for the first HC595 module
*/
void HC595a_send(char, char, char);
/**
Send data for the second HC595 module
*/
void HC595b_send(char, char, char);
// ------ Private variables -----------------------------------

// ------ PUBLIC variable definitions -------------------------

//--------------------------------------------------------------
// FUNCTION DEFINITIONS
//--------------------------------------------------------------
void HC595s_init() {
	if(wiringPiSetup() == -1){ //when initialize wiring failed,print message to the screen
		printf("setup wiringPi failed !");
		return; 
	}//end if
	//set pins to output so you can control the shift register
	pinMode(DS_PIN_a, OUTPUT);
	pinMode(STCP_PIN_a, OUTPUT);
	pinMode(SHCP_PIN_a, OUTPUT);
  //set pins to output so you can control the shift register
	pinMode(DS_PIN_b, OUTPUT);
	pinMode(STCP_PIN_b, OUTPUT);
	pinMode(SHCP_PIN_b, OUTPUT);
}//end HC595s_init
//--------------------------------
void HC595s_initState() {
  HC595a_send(BEGIN_STATE,BEGIN_STATE,BEGIN_STATE);
  HC595b_send(BEGIN_STATE,BEGIN_STATE,BEGIN_STATE);
}//end HC595s_init
//--------------------------------
//data will flow as FIFO
void HC595a_send(char firstByte, char midByte, char lastByte) { //send data to the first locker module
  digitalWrite(STCP_PIN_a, LOW); // LATCH_PIN low, make sure the LEDs don't change while you're sending in bits
  myShiftOut(DS_PIN_a, SHCP_PIN_a, MSBFIRST, lastByte); //DATA to the last 74HC595 in the chain -dataPin - clockPin - order - data
  myShiftOut(DS_PIN_a, SHCP_PIN_a, MSBFIRST, midByte); //DATA to the next 74HC595 in the chain -dataPin - clockPin - order - data
  myShiftOut(DS_PIN_a, SHCP_PIN_a, MSBFIRST, firstByte); //DATA to the first 74HC595 in the chain -dataPin - clockPin - order - data
  digitalWrite(STCP_PIN_a, HIGH);//take the latch pin high so the LEDs will light up   
}//end HC595a_send
//--------------------------------
//data will flow as FIFO
void HC595b_send(char firstByte, char midByte, char lastByte) { //send data to the second locker module
  digitalWrite(STCP_PIN_b, LOW); // LATCH_PIN low, make sure the LEDs don't change while you're sending in bits
  myShiftOut(DS_PIN_b, SHCP_PIN_b, MSBFIRST, lastByte); //DATA to the last 74HC595 in the chain -dataPin - clockPin - order - data
  myShiftOut(DS_PIN_b, SHCP_PIN_b, MSBFIRST, midByte); //DATA to the next 74HC595 in the chain -dataPin - clockPin - order - data
  myShiftOut(DS_PIN_b, SHCP_PIN_b, MSBFIRST, firstByte); //DATA to the first 74HC595 in the chain -dataPin - clockPin - order - data
  digitalWrite(STCP_PIN_b, HIGH);//take the latch pin high so the LEDs will light up   
}//end HC595b_send
//--------------------------------
void myShiftOut(uint8_t dataPin, uint8_t clockPin, uint8_t bitOrder, uint8_t val)
{
  uint8_t i;
  for (i = 0; i < 8; i++)  {
    if (bitOrder == LSBFIRST){
      digitalWrite(dataPin, !!(val & (1 << i)));
    } else {
      digitalWrite(dataPin, !!(val & (1 << (7 - i))));
    }//end if else

    digitalWrite(clockPin, HIGH);
    delayMicroseconds(1);
    digitalWrite(clockPin, LOW);
    delayMicroseconds(1);
  }//end for
}//end myShiftOut
//--------------------------------
#endif //__RASP_HC595_CPP
