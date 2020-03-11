/*------------------------------------------------------------*-
  Peripheral initialize functions file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  version 1.30 - 10/10/2019
 --------------------------------------------------------------
 * Perpherals drive by 74HC595 (6 units, 2 channel - 1 channel 3 units)
 * 
 -------------------------------------------------------------- */
#include "Rasp_HC595.h"

int main(void) {
  //printf("HC595 run!\n");
  HC595s_init();
  HC595s_initState();
  //printf("HC595 stop!\n");
}//end main
