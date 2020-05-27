/*------------------------------------------------------------*-
  RDM630/6300 125khz Card Reader - header file
  ESP32 CORE1 - APPLICATION CORE
  (c) An Minh Dao 2019
  version 3.00 - 25/02/2019
---------------------------------------------------------------
 *  PUBLIC FUNCTIONS CONTAIN:
 *  void RFID125_init();
 *  bool hasID();  //check if there is any new ID by interrupt
 *   
 *  PRIVATE FUNCTIONS CONTAIN:
 *  void RFID125_interrupt();
 *  void GetID();
 *  long hexstr_to_value(unsigned char *str, unsigned int str_length);
 * 
 *  CAUTION: must include config.h
 --------------------------------------------------------------*/
#ifndef _RFID_125KHZ_H
#define _RFID_125KHZ_H
#include "Arduino.h"
//#include "WiFi.h"

// ------ Public constants ------------------------------------
#define RF_INTERRUPT_PIN  27

typedef uint8_t uByte;
typedef uint16_t uInt;
typedef uint32_t uLong;

#ifdef ESP32_DEBUG // When this is active, every log will be execute.
  #ifndef SERIAL_OUTPUT
    #define SERIAL_OUTPUT
  #endif
  #ifndef WIFI_CHANGEABLE
    #define WIFI_CHANGEABLE
  #endif
  #ifndef SERIAL_BEGIN
    #define SERIAL_BEGIN()      {Serial.begin(115200);}
  #endif
  #define D_PRINT(...)       {Serial.print(__VA_ARGS__);}
  #define D_PRINTLN(...)     {Serial.println(__VA_ARGS__);}
  #define D_PRINTF(...)      {Serial.printf(__VA_ARGS__);}
#else
  #define D_PRINT(...)   {}
  #define D_PRINTLN(...) {}
  #define D_PRINTF(...)  {}
#endif

#ifdef WIFI_CHANGEABLE
  #ifndef SERIAL_BEGIN
    #define SERIAL_BEGIN()      {Serial.begin(115200);}
  #endif
#endif

#ifdef SERIAL_OUTPUT
  #ifndef SERIAL_BEGIN
    #define SERIAL_BEGIN()      {Serial.begin(115200);}
  #endif
  #define S_PRINT(...)       {Serial.print(__VA_ARGS__);}
  #define S_PRINTLN(...)     {Serial.println(__VA_ARGS__);}
  #define S_PRINTF(...)      {Serial.printf(__VA_ARGS__);}
#else
  #ifndef SERIAL_BEGIN
    #define SERIAL_BEGIN()  {}
  #endif
  #define S_PRINT(...)   {}
  #define S_PRINTLN(...) {}
  #define S_PRINTF(...)  {}
#endif


// ------ Public function prototypes --------------------------
void RFID125_init();
bool hasID(); //check if there is any new ID by interrupt
String getID();

// ------ Public variable -------------------------------------
//extern char  strID[];

#endif //_RFID_125KHZ_H
