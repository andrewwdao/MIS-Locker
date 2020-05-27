/*------------------------------------------------------------*-
  RFID125Khz sender - MASTER FILE
  (c) An Minh Dao 2019
  version 1.00 - 27/11/2019
---------------------------------------------------------------
*
* REMEMBER to define in c_cpp_properties.json as well
* 
--------------------------------------------------------------*/
#include "RFID_125Khz.h"

void setup() {
  Serial.begin(115200);
  RFID125_init();
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,HIGH);
  // Serial.println("System Ready!");
}

void loop() {
  if (hasID()) {
    Serial.print(getID());
    Serial.print("\r\n");
  }//end if
}
