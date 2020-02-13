/*------------------------------------------------------------*-
  Wiegand Reader - function file
  Tested with Gwiot 7304D2 RFID Reader(26 bit Wiegand mode) and RASPBERRY PI 3B+
  (c) Spiros Ioannou 2017
  (c) Minh-An Dao 2019
  version 1.10 - 25/10/2019
 --------------------------------------------------------------
 * RFID reader using Wiegand 26 protocol.
 * Use both 125Khz and 315Mhz Cards
 *
 *  ------ Pinout ------
 *  1(RED)    - VCC     - DC 9-12V
 *  2(BROWN)  - FORMAT  - Keep floating to use wiegand26, connect to GND to use weigang34
 *  3(BLUE)   - OUT     - 5V in normal condition, GND when card was scanned
 *  4(YELLOW) - Buzzer  - pull up automatically (5V), pull to GND to make it beep.
 *  5(ORANGE) - LED     - pull up automatically (5V) - RED, pull to GND to make it GREEN.
 *  6(GREEN)  - DATA0   - Wiegand DATA0 pin.
 *  7(WHITE)  - DATA1   - Wiegand DATA1 pin.
 *  8(BLACK)  - GND
 *
 * This is interrupt driven, no polling occurs.
 * After each bit is read, a timeout is set.
 * If timeout is reached read code is evaluated for correctness.
 *
 * Wiegand Bits:
 * pFFFFFFFFNNNNNNNNNNNNNNNNP
 * p: even parity of F-bits and leftmost 4 N-bits
 * F: Facility code
 * N: Card Number
 * P: odd parity of rightmost 12 N-bits
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
#ifndef __RFID_WIEGAND_C
#define __RFID_WIEGAND_C
#include "rfid_wiegand.h"

// ------ Private constants -----------------------------------
/* Defaults, change with command-line options */
#define D0_DEFAULT_PIN 3 // wiringPi pin
#define D1_DEFAULT_PIN 2 // wiringPi pin

#define WIEGAND_MAXBITS 40

/* Set some timeouts */
/* Wiegand defines:
 * a Pulse Width time between 20 μs and 100 μs (microseconds)
 * a Pulse Interval time between 200 μs and 20000 μs
 * Each bit takes 4-6 usec, so all 26 bit sequence would take < 200usec */
#define WIEGAND_BIT_INTERVAL_TIMEOUT_USEC 20000 /* interval between bits, typically 1000us */
// ------ Private function prototypes -------------------------
/**
DATA0 Interrupt Routine
*/
void d0_ISR(void);
/**
DATA1 Interrupt Routine
*/
void d1_ISR(void);
/**
Parse Wiegand 26bit format
Called wherever a new bit is read
bit: 0 or 1
*/
void add_bit_w26(int);
/**
Timeout from last bit read, sequence may be completed or stopped
If completed, then output the desired information
*/
void wiegand_timeout();
/**
Reset sequence of the wiegand data (reset bit counting variable)
*/
void wiegand_sequence_reset();
/**
get the time differences from bit to bit (ns)
*/
unsigned long get_bit_timediff_ns();
/**
timeout handler (usec), should fire after bit sequence has been read
*/
void reset_timeout_timer(long);
/**
Show ALL results out
*/
void rfid_showAll();

// ------ Private variables -----------------------------------
struct itimerval it_val;
struct sigaction sa;
static struct timespec wbit_tm; //for debug
int debug;
int in_system;

struct wiegand_data {
    unsigned char p0, p1;       //parity 0 , parity 1
    uint8_t facility_code;
    uint16_t card_code;
    uint32_t full_code;;
    int code_valid;
    unsigned long bitcount;     // bits read
} wds;
// ------ PUBLIC variable definitions -------------------------

//--------------------------------------------------------------
// FUNCTION DEFINITIONS
//--------------------------------------------------------------
void d0_ISR(void) {
    reset_timeout_timer(WIEGAND_BIT_INTERVAL_TIMEOUT_USEC);     //timeout waiting for next bit
    if (debug) {
        fprintf(stderr, "Bit:%02ld, Pulse 0, %ld us since last bit\n",
                wds.bitcount, get_bit_timediff_ns() / 1000);
        clock_gettime(CLOCK_MONOTONIC, &wbit_tm);
    }//end if
    add_bit_w26(0);
}//end d0_ISR
//--------------------------------------------------------------
void d1_ISR(void) {
    reset_timeout_timer(WIEGAND_BIT_INTERVAL_TIMEOUT_USEC);     //timeout waiting for next bit
    if (debug) {
        fprintf(stderr, "Bit:%02ld, Pulse 1, %ld us since last bit\n",
                wds.bitcount, get_bit_timediff_ns() / 1000);
        clock_gettime(CLOCK_MONOTONIC, &wbit_tm);
    }//end if
    add_bit_w26(1);
}//end d1_ISR
//--------------------------------------------------------------
void rfid_init(int d0pin,int d1pin,
               int input_debug, int input_in_system) {
    debug = input_debug;
    in_system = input_in_system;
    //-------------- Setup wiegand timeout handler -------------
    sigemptyset(&sa.sa_mask);
    sa.sa_handler = wiegand_timeout;;
    //sa.sa_flags = SA_SIGINFO;

    if (debug)
        fprintf(stderr, "\n");

    if (sigaction(SIGALRM, &sa, NULL) < 0) {
        perror("sigaction");
        // return 1;
    };
    // return 0;

    //---------------------- Setup GPIOs -----------------------
    wiringPiSetup();
    pinMode(d0pin, INPUT);
    pinMode(d1pin, INPUT);

    wiringPiISR(d0pin, INT_EDGE_FALLING, d0_ISR);
    wiringPiISR(d1pin, INT_EDGE_FALLING, d1_ISR);

    //-------------------- Reset sequence ---------------------
    wiegand_sequence_reset();
}//end rfid_init
//--------------------------------------------------------------
void add_bit_w26(int bit) {
    static int parity0 = 0;
    static int parity1 = 0;

    //---------------------Parity calculation
    if (wds.bitcount == 0) {
        parity0 = 0;
        parity1 = 0;
    }
    if (wds.bitcount > 0 && wds.bitcount <= 12) {
        parity0 += bit;
    }
    else if (wds.bitcount >= 13 && wds.bitcount <= 24) {
        parity1 += bit;
    }

    //---------------------Code calculation
    if (wds.bitcount == 0) {
        /* Reset */
        wds.code_valid = 0;
        wds.facility_code = 0;
        wds.card_code = 0;
        wds.p0 = bit; //parity
    }
    else if (wds.bitcount <= 8) {
        wds.facility_code <<= 1;
        if (bit)
            wds.facility_code |= 1;
    }
    else if (wds.bitcount < 25) {
        wds.card_code <<= 1;
        if (bit)
            wds.card_code |= 1;
    }
    else if (wds.bitcount == 25) {
        wds.p1 = bit;
        wds.full_code = wds.facility_code;
        wds.full_code = wds.full_code << 16;
        wds.full_code += wds.card_code;
        wds.code_valid = 1;
        //---------------------check parity
        if ((parity0 % 2) != wds.p0) {
            wds.code_valid = 0;
            if (debug) {
                fprintf(stderr, "Incorrect even parity bit (leftmost)\n");
            }
        }
        else if ((!(parity1 % 2)) != wds.p1) {
            wds.code_valid = 0;
            if (debug) {
                fprintf(stderr, "Incorrect odd parity bit (rightmost)\n");
            }
        }
    }// end else if wds.bitcount == 25
    else if (wds.bitcount > 25) {
        wds.code_valid = 0;
        wiegand_sequence_reset();
    }

    //---------------------Increase bit counting
    if (wds.bitcount < WIEGAND_MAXBITS) {
        wds.bitcount++;
    }
}//end add_bit_w26
//--------------------------------------------------------------
void wiegand_timeout() { //Timeout from last bit read, sequence may be completed or stopped
    if (debug)
        fprintf(stderr, "wiegand timeout\n");
    wiegand_sequence_reset();

    if ((!in_system)||debug) { //for testing the function
        rfid_showAll();
    } else {  //for usage inside the big system
        if (wds.code_valid) { //if the received code is valid
            printf("0x%X\n", wds.full_code);
            fflush(stdout);
        } else { //if the received code is NOT valid
            printf("CHECKSUM_FAILED\n");
            fflush(stdout);
        }//end if else
    }//end if else
} //end wiegand_timeout
//--------------------------------------------------------------
void wiegand_sequence_reset() {
    wds.bitcount = 0;

}//end wiegand_sequence_reset
//--------------------------------------------------------------
unsigned long get_bit_timediff_ns() {
    struct timespec now, delta;
    unsigned long tdiff;

    clock_gettime(CLOCK_MONOTONIC, &now);
    delta.tv_sec = now.tv_sec - wbit_tm.tv_sec;
    delta.tv_nsec = now.tv_nsec - wbit_tm.tv_nsec;

    tdiff = delta.tv_sec * 1000000000 + delta.tv_nsec;

    return tdiff;
}//end get_bit_timediff_ns
//--------------------------------------------------------------
void reset_timeout_timer(long usec) { //timeout handler, should fire after bit sequence has been read
    it_val.it_value.tv_sec = 0;
    it_val.it_value.tv_usec = usec;

    it_val.it_interval.tv_sec = 0;
    it_val.it_interval.tv_usec = 0;

    if (setitimer(ITIMER_REAL, &it_val, NULL) == -1) {
        perror("setitimer");
        exit(1);
    }
}//end reset_timeout_timer
//--------------------------------------------------------------
void rfid_showAll() {
    printf("\n*** Code Valid: %d\n", wds.code_valid);
    printf("*** Facility code: %d(dec) 0x%X\n", wds.facility_code,
           wds.facility_code);
    printf("*** Card code: %d(dec) 0x%X\n", wds.card_code, wds.card_code);
    printf("*** Full code: %d\n", wds.full_code);
    printf("*** Parity 0:%d Parity 1:%d\n\n", wds.p0, wds.p1);
    fflush(stdout);
}//end rfid_showAll
//--------------------------------------------------------------
void rfid_showUsage() {
    printf("\nHow to use:\n");
    printf("Type in the command line:\n");
    printf("\n\t./rfid_main [-d] [-h] [-a] [-0 D0-pin] [-1 D1-pin]\n\n");
    printf("With:\n");
    printf("\t-d : debug mode\n");
    printf("\t-h : help\n");
    printf("\t-a : dumb all received information out\n");
    printf("\t-0 D0-pin: GPIO pin for data0 pulse (wiringPi pin)\n");
    printf("\t-1 D1-pin: GPIO pin for data1 pulse (wiringPi pin)\n\n");
    fflush(stdout);
}//end rfid_showUsage
//--------------------------------------------------------------
#endif //__RFID_WIEGAND_C
