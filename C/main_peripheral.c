/*------------------------------------------------------------*-
  MAIN - functions file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  version 1.00 - 24/09/2019
 --------------------------------------------------------------
 * This code use the TMC2208 as the driver for the stepper.
 * Other Driver (A4988, DRV8825) should work fine too.
 * You just need to calibrate the MIN_DELAY(us) and MAX_DELAY(us)
 * in Rasp_Stepper.cpp to fit those driver.
 -------------------------------------------------------------- */
#include "Rasp_HC595.h"

int main(int dumbInt,char **InputChar) {
  char*  lastByte1  = InputChar[1];
  char*  midByte1   = InputChar[2];
  char*  firstByte1 = InputChar[3];

  char*  lastByte2  = InputChar[4];
  char*  midByte2   = InputChar[5];
  char*  firstByte2 = InputChar[6];
  printf("HC595 run!\n");
  HC595s_init();
  HC595a_send(0x00, 0x00, 0b00000100);
  HC595b_send(0x00, 0x00, 0b00000100);
  printf("HC595 stop!\n");
}//end main
