/*------------------------------------------------------------*-
  Weigang Reader - Gwiot 7304D2 - header file
  RASPBERRY PI 3B+
  (c) Minh-An Dao 2019
  (c) Alperen Güman 2017
  version 1.00 - 24/10/2019
 --------------------------------------------------------------
 * RFID reader using Weigang 26 protocol.
 * Use both 125Khz and 315Mhz Cards
 *  
 *  ------ Pinout ------
 *  1(RED)    - VCC     - DC 9-12V
 *  2(BROWN)  - FORMAT  - Keep floating to use weigang26, connect to GND to use weigang34
 *  3(BLUE)   - OUT     - 5V in normal condition, GND when card was scanned
 *  4(YELLOW) - Buzzer  - pull up automatically (5V), pull to GND to make it beep.
 *  5(ORANGE) - LED     - pull up automatically (5V) - RED, pull to GND to make it GREEN.
 *  6(GREEN)  - DATA0   - Weigang DATA0 pin.
 *  7(WHITE)  - DATA1   - Weigang DATA1 pin.
 *  8(BLACK)  - GND
 * 
 -------------------------------------------------------------- */
#ifndef __RASP_GWIOT_7304D2_H
#define __RASP_GWIOT_7304D2_H
#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <time.h>
#include <unistd.h>
#include <memory.h>

// ------ Public constants ------------------------------------

// ------ Public function prototypes --------------------------
/**
Initialize rfid module and put it in the w()
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




int wiegandInit(int d0pin, int d1pin) {
    // Setup wiringPi
    wiringPiSetup() ;
    pinMode(d0pin, INPUT);
    pinMode(d1pin, INPUT);
    pinMode(PIN_SOUND, OUTPUT);

    wiringPiISR(d0pin, INT_EDGE_FALLING, getData0);
    wiringPiISR(d1pin, INT_EDGE_FALLING, getData1);
}

void wiegandReset() {
    memset((void *)__wiegandData, 0, MAXWIEGANDBITS);
    __wiegandBitCount = 0;
}

int wiegandGetPendingBitCount() {
    struct timespec now, delta;
    clock_gettime(CLOCK_MONOTONIC, &now);
    delta.tv_sec = now.tv_sec - __wiegandBitTime.tv_sec;
    delta.tv_nsec = now.tv_nsec - __wiegandBitTime.tv_nsec;

    if ((delta.tv_sec > 1) || (delta.tv_nsec > READERTIMEOUT))
        return __wiegandBitCount;

    return 0;
}

int wiegandReadData(void* data, int dataMaxLen) {
    if (wiegandGetPendingBitCount() > 0) {
        int bitCount = __wiegandBitCount;
        int byteCount = (__wiegandBitCount / 8) + 1;
        memcpy(data, (void *)__wiegandData, ((byteCount > dataMaxLen) ? dataMaxLen : byteCount));

        wiegandReset();
        return bitCount;
    }
    return 0;
}

void printCharAsBinary(unsigned char ch) {
    int i;
    FILE * fp;
    fp = fopen("output","a");

    for (i = 0; i < 8; i++) {
        printf("%d", (ch & 0x80) ? 1 : 0);
        fprintf(fp, "%d", (ch & 0x80) ? 1 : 0);
        ch <<= 1;
    }

    fclose(fp);
}


void makeBeep(int millisecs, int times){
    int i;
    for (i = 0; i < times; i++) {
        digitalWrite (PIN_SOUND,  LOW);
        delay(millisecs);
        digitalWrite (PIN_SOUND, HIGH);
        delay(millisecs/2);
    }
}



void main(void) {
    int i;

    wiegandInit(PIN_0, PIN_1);


    while(1) {
        int bitLen = wiegandGetPendingBitCount();
        if (bitLen == 0) {
            usleep(5000);
        } else {
            char data[100];
            char string1[100];
            bitLen = wiegandReadData((void *)data, 100);
            int bytes = bitLen / 8 + 1;
            FILE *fp;
            fp = fopen("output","a");
            printf("%lu ", (unsigned long)time(NULL));
            fprintf(fp, "%lu ", (unsigned long)time(NULL));
            printf("Read %d bits (%d bytes): ", bitLen, bytes);
            fprintf(fp, "Read %d bits (%d bytes): ", bitLen, bytes);
            for (i = 0; i < bytes; i++)
                printf("%02X", (int)data[i]);
            for (i = 0; i < bytes; i++)
                fprintf(fp, "%02X", (int)data[i]);

            printf(" : ");
            fprintf(fp, " : ");
            fclose(fp);
            for (i = 0; i < bytes; i++)
                printCharAsBinary(data[i]);
            fp = fopen("output","a");
            printf("\n");
            fprintf(fp, "\n");
            fclose(fp);
            makeBeep(200, 1);
        }
    }
}

#endif //__RASP_GWIOT_7304D2_H