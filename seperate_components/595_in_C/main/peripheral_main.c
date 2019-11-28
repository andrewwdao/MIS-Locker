/*------------------------------------------------------------*-
  Peripheral main functions file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  version 1.30 - 10/10/2019
 --------------------------------------------------------------
 * Perpherals drive by 74HC595 (6 units, 2 channel - 1 channel 3 units)
 * 
 -------------------------------------------------------------- */
#include "Rasp_HC595.h"

int main(int dumbInt,char **InputChar) {
  char*  firstByte1  = InputChar[1];
  char*  midByte1   = InputChar[2];
  char*  lastByte1 = InputChar[3];

  char*  firstByte2  = InputChar[4];
  char*  midByte2   = InputChar[5];
  char*  lastByte2 = InputChar[6];
  //printf("HC595 run!\n");
  HC595s_init();
  HC595a_send(atoi(firstByte1), atoi(midByte1), atoi(lastByte1));
  HC595b_send(atoi(firstByte2), atoi(midByte2), atoi(lastByte2));
  //printf("HC595 stop!\n");
}//end main
