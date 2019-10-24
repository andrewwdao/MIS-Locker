/*
 * Wiegand data reader with Raspberry Pi
 * Tested with RPi Model B rev2, and an 26bit Wiegand Cards
 * Spiros Ioannou 2017
 *
 * This is interrupt drivern, no polling occurs. 
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
 * Compile with: gcc wiegand_rpi.c   -lwiringPi -lpthread -lrt  -Wall -o wiegand_rpi -O
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <memory.h>
#include <stdint.h>
#include <sys/time.h>
#include <signal.h>
#include <wiringPi.h>

/* Defaults, change with command-line options */
#define D0_PIN 0
#define D1_PIN 2

#define WIEGANDMAXBITS 40

/* Set some timeouts */

/* Wiegand defines:
 * a Pulse Width time between 20 μs and 100 μs (microseconds)
 * a Pulse Interval time between 200 μs and 20000 μsec
 */

/* Each bit takes 4-6 usec, so all 26 bit sequence would take < 200usec */
#define WIEGAND_BIT_INTERVAL_TIMEOUT_USEC 20000 /* interval between bits, typically 1000us */

struct itimerval it_val;
struct sigaction sa;

struct wiegand_data {
    unsigned char p0, p1;       //parity 0 , parity 1
    uint8_t facility_code;
    uint16_t card_code;
    uint32_t full_code;;
    int code_valid;
    unsigned long bitcount;     // bits read
} wds;

struct option_s {
    int d0pin;
    int d1pin;
    int debug;
} options;

void show_code();
void wiegand_sequence_reset();
void reset_timeout_timer(long usec);
void gpio_init(int d0pin, int d1pin);

static struct timespec wbit_tm; //for debug

/* Timeout from last bit read, sequence may be completed or stopped */
void wiegand_timeout() {
    if (options.debug)
        fprintf(stderr, "wiegand_timeout()\n");
    wiegand_sequence_reset();
    show_code();
}

void show_code() {
    printf("\n");
    printf("*** Code Valid: %d\n", wds.code_valid);
    printf("*** Facility code: %d(dec) 0x%X\n", wds.facility_code,
           wds.facility_code);
    printf("*** Card code: %d(dec) 0x%X\n", wds.card_code, wds.card_code);
    printf("*** Full code: %d\n", wds.full_code);
    printf("*** Parity 0:%d Parity 1:%d\n", wds.p0, wds.p1);
    fflush(stdout);
}

int setup_wiegand_timeout_handler() {
    sigemptyset(&sa.sa_mask);
    sa.sa_handler = wiegand_timeout;;
    //sa.sa_flags = SA_SIGINFO;

    if (options.debug)
        fprintf(stderr, "\n");

    if (sigaction(SIGALRM, &sa, NULL) < 0) {
        perror("sigaction");
        return 1;
    };
    return 0;
}

/* Parse Wiegand 26bit format 
 * Called wherever a new bit is read
 * bit: 0 or 1
 */
void add_bit_w26(int bit) {
    static int parity0 = 0;
    static int parity1 = 0;

    //Parity calculation
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
    //Code calculation
    if (wds.bitcount == 0) {
        /* Reset */
        wds.code_valid = 0;
        wds.facility_code = 0;
        wds.card_code = 0;
        wds.p0 = bit;           //parity
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
        //check parity
        if ((parity0 % 2) != wds.p0) {
            wds.code_valid = 0;
            if (options.debug) {
                fprintf(stderr, "Incorrect even parity bit (leftmost)\n");
            }
        }
        else if (!(parity1 % 2) != wds.p1) {
            wds.code_valid = 0;
            if (options.debug) {
                fprintf(stderr, "Incorrect odd parity bit (rightmost)\n");
            }
        }

    }
    else if (wds.bitcount > 25) {
        wds.code_valid = 0;
        wiegand_sequence_reset();

    }

    if (wds.bitcount < WIEGANDMAXBITS) {
        wds.bitcount++;
    }

}

unsigned long get_bit_timediff_ns() {
    struct timespec now, delta;
    unsigned long tdiff;

    clock_gettime(CLOCK_MONOTONIC, &now);
    delta.tv_sec = now.tv_sec - wbit_tm.tv_sec;
    delta.tv_nsec = now.tv_nsec - wbit_tm.tv_nsec;

    tdiff = delta.tv_sec * 1000000000 + delta.tv_nsec;

    return tdiff;

}

void d0_pulse(void) {
    reset_timeout_timer(WIEGAND_BIT_INTERVAL_TIMEOUT_USEC);     //timeout waiting for next bit
    if (options.debug) {
        fprintf(stderr, "Bit:%02ld, Pulse 0, %ld us since last bit\n",
                wds.bitcount, get_bit_timediff_ns() / 1000);
        clock_gettime(CLOCK_MONOTONIC, &wbit_tm);
    }
    add_bit_w26(0);
}

void d1_pulse(void) {
    reset_timeout_timer(WIEGAND_BIT_INTERVAL_TIMEOUT_USEC);     //timeout waiting for next bit
    if (options.debug) {
        fprintf(stderr, "Bit:%02ld, Pulse 1, %ld us since last bit\n",
                wds.bitcount, get_bit_timediff_ns() / 1000);
        clock_gettime(CLOCK_MONOTONIC, &wbit_tm);
    }
    add_bit_w26(1);
}

void wiegand_sequence_reset() {
    wds.bitcount = 0;
}

/* timeout handler, should fire after bit sequence has been read */
void reset_timeout_timer(long usec) {
    it_val.it_value.tv_sec = 0;
    it_val.it_value.tv_usec = usec;

    it_val.it_interval.tv_sec = 0;
    it_val.it_interval.tv_usec = 0;

    if (setitimer(ITIMER_REAL, &it_val, NULL) == -1) {
        perror("setitimer");
        exit(1);
    }
}

void gpio_init(int d0pin, int d1pin) {

    wiringPiSetup();
    pinMode(d0pin, INPUT);
    pinMode(d1pin, INPUT);

    wiringPiISR(d0pin, INT_EDGE_FALLING, d0_pulse);
    wiringPiISR(d1pin, INT_EDGE_FALLING, d1_pulse);

}

void show_usage() {
    printf("Wiegand Reader (https://bitbucket.org/sivann/wiegand_read)\n");
    printf("Usage: wiegand_read [-d] [-0 D0-pin] [-1 D1-pin]\n");
    printf("\t-d\t\tdebug\n");
    printf("\t-0\t\tGPIO pin for data0 pulse\n");
    printf("\t-1\t\tGPIO pin for data1 pulse\n");
    printf("\tCheck http://wiringpi.com/pins for WiringPi pin numbers\n");
    printf("\n");
}

int main(int argc, char *argv[]) {
    int opt;

    /* defaults */
    options.d0pin = D0_PIN;
    options.d1pin = D1_PIN;
    options.debug = 0;

    /* Parse Options */
    while ((opt = getopt(argc, argv, "d0:1:")) != -1) {
        switch (opt) {
        case 'd':
            options.debug++;
            break;
        case '0':
            options.d0pin = atoi(optarg);
            break;
        case '1':
            options.d1pin = atoi(optarg);
            break;
        case 'h':
            show_usage();
            exit(0);
            break;
        default:               /* '?' */
            show_usage();
            exit(EXIT_FAILURE);
        }
    }

    setup_wiegand_timeout_handler();
    gpio_init(options.d0pin, options.d1pin);
    wiegand_sequence_reset();

    while (1) {
        pause();
        printf("\nAfter Pause\n\n");
    }
}
