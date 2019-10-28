/*------------------------------------------------------------*-
  Buzzer main functions file
  Tested on Gwiot 7304D2 RFID Reader(26 bit Wiegand mode) and RASPBERRY PI 3B+
    (c) Minh-An Dao 2019
  version 1.00 - 28/10/2019
 --------------------------------------------------------------
 *
 * Usage:
 * ./buzzer_main [-d] [delay] [-b] [beep] [-p] [pin]
 *  With:
 *  -delay: buzzer ON time
 *  -beep : times to beep
 *  -pin: new buzzer pin (wiringPi pin)
 *
 -------------------------------------------------------------- */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <signal.h>
#include <wiringPi.h>

/* Defaults, change with command-line options */
#define BUZZER_PIN   0 // wiringPi pin -BCM pin 17
#define BUZZER_DELAY 300 //ms

void buzzer_showUsage();
void buzzer_start(int buzDelay,int buzTimes,int buzPin);

int main(int argc, char *argv[]) {
    /* defaults */
    int buzzer_delay = BUZZER_DELAY;
    int beep_times = 1;
    int buzzer_pin = BUZZER_PIN;

    /* Parse Options */
    int opt;
    while ((opt = getopt(argc, argv, "p:b:")) != -1) {
        switch (opt) {
        case 'd':
            buzzer_delay = atoi(optarg);
            break;
        case 'b':
            beep_times = atoi(optarg);
            break;
        case 'p':
            buzzer_pin = atoi(optarg);
            break;
        default: /* unknown command */
            buzzer_showUsage();
            exit(0);
        }//end switch case
    }//end while

    buzzer_start(buzzer_delay,beep_times,buzzer_pin);

}//end main

void buzzer_showUsage() {
    printf("\nHow to use:\n");
    printf("Type in the command line:\n");
    printf("\n\t./buzzer_main [-d] [delay] [-b] [beep] [-p] [pin]\n\n");
    printf("With:\n");
    printf("\t-delay: buzzer ON time\n");
    printf("\t-beep : times to beep\n");
    printf("\t-pin: new buzzer pin (wiringPi pin)\n");
    fflush(stdout);
}//end rfid_showUsage

void buzzer_start(int buzDelay,int buzTimes,int buzPin) {
    //---------------------- Setup GPIOs -----------------------
    wiringPiSetup();
    pinMode(buzPin, OUTPUT);
    for (int i=0;i<buzTimes;i++) {
        digitalWrite(buzPin, LOW); //BEEP
        delay(buzDelay);
        digitalWrite(buzPin, HIGH); //NO BEEP
        delay(buzDelay);
    }//end for
}//end buzzer_start