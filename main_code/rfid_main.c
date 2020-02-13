/*------------------------------------------------------------*-
  RFID reader main functions file
  Tested with Gwiot 7304D2 RFID Reader(26 bit Wiegand mode) and RASPBERRY PI 3B+
    (c) Minh-An Dao 2019
    (c) Spiros Ioannou 2017
  version 1.10 - 25/10/2019
 --------------------------------------------------------------
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
#include "rfid_wiegand.h"

/* Defaults, change with command-line options */
#define D0_PIN 3 // wiringPi pin
#define D1_PIN 2 // wiringPi pin

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
    while ((opt = getopt(argc, argv, "dha0:1:")) != -1) {
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
        pause(); //pause to wait for ISR and not consuming system memory
    }//end while
}//end main

