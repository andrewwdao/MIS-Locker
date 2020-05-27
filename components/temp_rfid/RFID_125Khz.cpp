/*------------------------------------------------------------*-
  RDM630/6300 125khz Card Reader - functions file
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
 --------------------------------------------------------------*/
#ifndef _RFID_125KHZ_CPP
#define _RFID_125KHZ_CPP
#include "RFID_125Khz.h"

// ------ Private constants -----------------------------------
const char DATA_SIZE     PROGMEM = 10; // 10byte data (2byte version + 8byte tag)
const char BUFFER_SIZE   PROGMEM = 14; // RFID DATA FRAME FORMAT: 1byte head (value: 2), 10byte data (2byte version + 8byte tag), 2byte checksum, 1byte tail (value: 3)
const char CHECKSUM_SIZE PROGMEM = 2;  // 2byte checksum
const int  RF_DEBOUNCE   PROGMEM = 1000; //debounce for 2s
#ifdef ESP32_DEBUG
const char DATA_VERSION  PROGMEM = 2; // 2byte version (actual meaning of these two bytes may vary)
const char DATA_TAG      PROGMEM = 8; // 8byte tag
#endif

// ------ Private function prototypes -------------------------
static void RFID125_interrupt();
static void collectID();
static long hexstr_to_value(uByte*, uInt);

// ------ Private variables -----------------------------------
static uByte   buffer[BUFFER_SIZE]; // used to store an incoming data frame 
static uByte   buffer_index = 0;
static bool    gotID = false;
static bool    gotID_count = false;
static uLong   lastmillis_rf;
static char    strID[DATA_SIZE+1];
// ------ PUBLIC variable definitions -------------------------

//--------------------------------------------------------------
// FUNCTION DEFINITIONS
//--------------------------------------------------------------
void RFID125_init() {//RF INITIALIZE
  Serial2.begin(9600); //default baudrate for RDM630/6300
  pinMode(RF_INTERRUPT_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN),RFID125_interrupt, FALLING); //run on core1
  //D_PRINTLN(F("Module RFID 125Khz ready!"));
}//end cardReader_init

bool hasID() { //check if there is any new ID by interrupt
  if (gotID) { //this is to make sure the job is proceed imediately, and after the job done, we care about the debounce and re-activate the interrupt
    gotID=false;
    gotID_count=true;
    return true;
  }//end if gotID
//WE HAVE TO DO THIS INSTEAD OF DEBOUNCE DIRECTLY BECAUSE THE DEBOUNCE TIME IS HIGH!
  if (gotID_count) { 
    if ((millis()-lastmillis_rf)>RF_DEBOUNCE) {//debounce for RF_DEBOUNCE ms
      gotID_count=false;
      Serial2.begin(9600);
      attachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN),RFID125_interrupt, FALLING);
    }//end if
  }//end if
  return false;
}//end hasID

String getID() {
  return (String)strID;
}//end getID
/////////////////////////////////////////////////// RDM6300 INTERRUPT ////////////////////////////////////////////////////////
static void RFID125_interrupt() { //CAUTION: must change Watchdog Interrupt Timeout configurations to 1000ms before proceed!! - make change using esp-idf
    detachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN));
    lastmillis_rf=millis();
    uint8_t ssvalue;
    uint8_t count=0;
    while (1) {
      ssvalue = Serial2.read(); // read
      if (ssvalue==2) {
        count=0;
        buffer_index = 0;
        buffer[buffer_index++] = ssvalue; // everything is alright => copy first letter into buffer
        while (1) {
          ssvalue = Serial2.read(); // read
          buffer[buffer_index++] = ssvalue; // everything is alright => copy current value to buffer
          if (ssvalue==3) {
            if (buffer_index == BUFFER_SIZE) {
              collectID();
              // gotID=true;
              Serial2.end();
              return;
            }//end if
            else {
              D_PRINTLN(F("Something is wrong...starting again..."));
              attachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN), RFID125_interrupt, FALLING);
              return;
            }//end else
          }//end ssvalue==3 (end of signal)
          if (buffer_index > BUFFER_SIZE) { // checking for a buffer overflow (It's very unlikely that an buffer overflow comes up!)
            D_PRINTLN(F("Error: Buffer overflow detected!"));
            attachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN), RFID125_interrupt, FALLING);
            return;
          }//end if
          if (count++>13){attachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN), RFID125_interrupt, FALLING); return;} //something is wrong so no ending signal (3) is detected (14 signal, first one have been count already, so if it bigger than 13, that means it have more than 14 elements)
        }//end while
      }//end ssvalue==2 (begin signal)

      if (count++==20) {attachInterrupt(digitalPinToInterrupt(RF_INTERRUPT_PIN), RFID125_interrupt, FALLING); return;} //no data was read
  }//end while
}//end interrupt
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*total 14 byte data: 1 byte begin (head) + 10 byte data + 2 byte checksum + 1 byte end (tail)*/
static void collectID() {
  unsigned char *msg_data = buffer + 1; //13 byte, 10 byte data, 2 byte checksum, 1 byte tail
  #ifdef ESP32_DEBUG
  unsigned char *msg_data_tag = buffer + 3; //11 byte, 8 byte data, 2 byte checksum, 1 byte tail
  #endif
  unsigned char *msg_checksum = buffer + 11; // 3 byte, 2 byte checksum, 1 byte tail
  volatile long checksum = 0;
  for (int i = 0; i < DATA_SIZE; i+= CHECKSUM_SIZE) {
    volatile long val = hexstr_to_value(msg_data + i, CHECKSUM_SIZE);
    checksum ^= val;
  }//end for
  boolean good = (checksum == hexstr_to_value(msg_checksum, CHECKSUM_SIZE))? true:false; //compare calculated checksum to retrieved checksum

  if (good) {//checksum return good value
    for (uint8_t i = 0; i < DATA_SIZE;i++) {
      strID[i] = msg_data[i];
    }//end for
    strID[10]='\0'; //equal DATA_SIZE
  if (((String)strID)!="0000000000") {
    gotID=true;
  } else {
    gotID=false;
    return;
  }//end else if

     //singleBeep(100); //cannot use here because of the interrupt handle <300ms
    S_PRINTLN();
    S_PRINTLN(F("--------"));
    D_PRINTLN(F("Checksum PASSED "));
    S_PRINT(F("Full Identity (HEX): "));
    S_PRINTLN(getID());

    #ifdef ESP32_DEBUG
    Serial.print(F("Tag only (HEX): "));
    for (int i = 0; i < DATA_TAG; ++i) {
      Serial.print(char(msg_data_tag[i]));
    }//end for
    Serial.println();
    Serial.print(F("Card Version (HEX): "));
    for (int i = 0; i < DATA_VERSION; ++i) {
      Serial.print(char(msg_data[i]));
    }//end for
    Serial.println();

    long tag = hexstr_to_value(msg_data_tag,DATA_TAG);
    Serial.print(F("Decimal Tag: "));
    Serial.println(tag);

    Serial.print(F("Checksum Code (HEX)(matched): "));
    for (int i = 0; i < CHECKSUM_SIZE; ++i) {
      Serial.print(char(msg_checksum[i]));
    }//end for
    Serial.println();
    #endif
  }//end if
  else {//checksum return bad value, do nothing but pop up message
    D_PRINTLN(F("Checksum FAILED "));
    D_PRINT(F("Original Checksum code: "));
    #ifdef ESP32_DEBUG
    for (int i = 0; i < CHECKSUM_SIZE; ++i) {
      Serial.print(char(msg_checksum[i]));
    }//end for
    #endif
    D_PRINT(F(". Result recieved: "));
    D_PRINT(checksum, HEX); D_PRINTLN();
    D_PRINTLN(F("Please scan your ID card again!"));
  }//end else
  D_PRINTLN(F("--------"));
}//end GetID

static long hexstr_to_value(uByte *str, uInt str_length) { // converts a hexadecimal value (encoded as ASCII string) to a numeric value
  //converting an a part of an array into a string (string is an array with null at the end)
  char* copy = (char*)malloc((sizeof(char) * str_length) + 1); 
  memcpy(copy, str, sizeof(char) * str_length);
  copy[str_length] = '\0'; 
  // the variable "copy" is a copy of the parameter "str". "copy" has an additional '\0' element to make sure that "str" is null-terminated.
  long value = strtol(copy, NULL, 16);  // strtol converts a null-terminated string to a long value
  free(copy); // clean up 
  return value;
}//end hex string to value


#endif //_RFID_125KHZ_CPP
