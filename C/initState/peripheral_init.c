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

int main(void) {
  //printf("HC595 run!\n");
  HC595s_init();
  HC595s_initState();
  //printf("HC595 stop!\n");
}//end main
