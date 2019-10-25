/*------------------------------------------------------------*-
  RFID reader main functions file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  version 1.30 - 10/10/2019
 --------------------------------------------------------------
 *
 * 
 -------------------------------------------------------------- */
#include "rfid_wiegand.h"

/* Defaults, change with command-line options */
#define D0_PIN 6
#define D1_PIN 10

struct option_s {
    int d0pin;
    int d1pin;
    int debug;
    int in_system;
} options;

int main(int argc, char *argv[]) {
    /* defaults */
    options.d0pin = D0_PIN;
    options.d1pin = D1_PIN;
    options.debug = 0;
    options.in_system = 1;

    /* Parse Options */
    int opt;
    while ((opt = getopt(argc, argv, "d0:1:")) != -1) {
        switch (opt) {
        case 'd':
            options.debug++;
            break;
        case 'h':
            rfid_showUsage();
            exit(0);
            break;
        case 'a':
            options.in_system = 0; //for testing the function - dumb all info out
            break;
        case '0':
            options.d0pin = atoi(optarg);
            break;
        case '1':
            options.d1pin = atoi(optarg);
            break;

        default: /* unknown command */
            rfid_showUsage();
            exit(0);
        }//end switch case
    }//end while

    rfid_init(options.d0pin,
              options.d1pin,
              options.debug,
              options.in_system);

    while (1) {
        pause();
        printf("\nAfter Pause\n\n");
    }//end while
}//end main

//int main(int dumbInt,char **InputChar) {
//  char*  firstByte1  = InputChar[1];
//  char*  midByte1   = InputChar[2];
//  char*  lastByte1 = InputChar[3];
//
//  char*  firstByte2  = InputChar[4];
//  char*  midByte2   = InputChar[5];
//  char*  lastByte2 = InputChar[6];
//  //printf("HC595 run!\n");
//  HC595s_init();
//  HC595a_send(atoi(firstByte1), atoi(midByte1), atoi(lastByte1));
//  HC595b_send(atoi(firstByte2), atoi(midByte2), atoi(lastByte2));
//  //printf("HC595 stop!\n");
//}//end main
