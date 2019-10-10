"""------------------------------------------------------------*-
  ADS1115 ADC module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Carter Nelson 2017
  (c) Karl-Petter Lindegaard 2017
  version 1.00 - 08/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import ADC.ads1115 as ADS
from ADC.analog_in import AnalogIn

# ---------------------------- Private Parameters:
ACTIVATE_MODULE02 = False
# -----Address and Screen parameter:
ADS_ADDRESS = 0x48
BUTTON = ADS.P0
SWITCH_M1 = ADS.P1
SWITCH_M2 = ADS.P2

# This adc value may have to be changed if changing power supply
NO_PRESS_MIN = ALL_CLOSED_MIN = 25000
NO_PRESS_MAX = ALL_CLOSED_MAX = 30000

# This adc value may have to be changed if changing power supply
CANCEL_MIN = 0
CANCEL_MAX = 500
UP_MIN = 1000
UP_MAX = 1500
DOWN_MIN = 2000
DOWN_MAX = 2500
OK_MIN = 3000
OK_MAX = 3500

# This adc value may have to be changed if changing power supply
DOOR01_MIN = 0
DOOR01_MAX = 500
DOOR02_MIN = 0
DOOR02_MAX = 500
DOOR03_MIN = 0
DOOR03_MAX = 500
DOOR04_MIN = 0
DOOR04_MAX = 500
DOOR05_MIN = 0
DOOR05_MAX = 500
DOOR06_MIN = 0
DOOR06_MAX = 500
DOOR07_MIN = 0
DOOR07_MAX = 500
DOOR08_MIN = 0
DOOR08_MAX = 500
DOOR09_MIN = 0
DOOR09_MAX = 500
DOOR10_MIN = 0
DOOR10_MAX = 500

DOOR11_MIN = 0
DOOR11_MAX = 500
DOOR12_MIN = 0
DOOR12_MAX = 500
DOOR13_MIN = 0
DOOR13_MAX = 500
DOOR14_MIN = 0
DOOR14_MAX = 500
DOOR15_MIN = 0
DOOR15_MAX = 500
DOOR16_MIN = 0
DOOR16_MAX = 500
DOOR17_MIN = 0
DOOR17_MAX = 500
DOOR18_MIN = 0
DOOR18_MAX = 500
DOOR19_MIN = 0
DOOR19_MAX = 500
DOOR20_MIN = 0
DOOR20_MAX = 500


class adc_read:
    def __init__(self, address=ADS_ADDRESS):
        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1115(address)


class adc_button(adc_read):
    def __init__(self):
        super().__init__()
        self.button = AnalogIn(self.ads, BUTTON)

    def read(self):
        current_val = self.button.value
        if NO_PRESS_MIN < current_val < NO_PRESS_MAX:  # no press at all
            return "BUT_NO_PRESS"
        if CANCEL_MIN < current_val < CANCEL_MAX:  # cancel button
            return "BUT_CANCEL"
        if UP_MIN < current_val < UP_MAX:  # up button
            return "BUT_UP"
        if DOWN_MIN < current_val < DOWN_MAX:  # down button
            return "BUT_DOWN"
        if OK_MIN < current_val < OK_MAX:  # ok button
            return "BUT_OK"
        return "ERROR"


class adc_switches(adc_read):
    def __init__(self):
        super().__init__()
        if ACTIVATE_MODULE02:  # Module02 also activated
            self.switchesM1 = AnalogIn(self.ads, SWITCH_M1)
            self.switchesM2 = AnalogIn(self.ads, SWITCH_M2)
        else:  # only Module01 is activated
            self.switchesM1 = AnalogIn(self.ads, SWITCH_M1)

    def read(self):
        current_valM1 = self.switchesM1.value
        if ACTIVATE_MODULE02:
            current_valM2 = self.switchesM2.value
            if (ALL_CLOSED_MIN < current_valM1 < ALL_CLOSED_MAX) and \
               (ALL_CLOSED_MIN < current_valM2 < ALL_CLOSED_MAX):  # all doors closed
                return "ALL_CLOSED"
            # first check module02
            if DOOR11_MIN < current_valM2 < DOOR11_MAX:  # door11
                return "DOOR11"
            if DOOR12_MIN < current_valM2 < DOOR12_MAX:  # door12
                return "DOOR12"
            if DOOR13_MIN < current_valM2 < DOOR13_MAX:  # door13
                return "DOOR13"
            if DOOR14_MIN < current_valM2 < DOOR14_MAX:  # door14
                return "DOOR14"
            if DOOR15_MIN < current_valM2 < DOOR15_MAX:  # door15
                return "DOOR15"
            if DOOR16_MIN < current_valM2 < DOOR16_MAX:  # door16
                return "DOOR16"
            if DOOR17_MIN < current_valM2 < DOOR17_MAX:  # door17
                return "DOOR17"
            if DOOR18_MIN < current_valM2 < DOOR18_MAX:  # door18
                return "DOOR18"
            if DOOR19_MIN < current_valM2 < DOOR19_MAX:  # door19
                return "DOOR19"
            if DOOR20_MIN < current_valM2 < DOOR20_MAX:  # door20
                return "DOOR20"
        else:
            if ALL_CLOSED_MIN < current_valM1 < ALL_CLOSED_MAX:  # all doors closed
                return "MODULE01_ALL_CLOSED"
        # now check Module01
        if DOOR01_MIN < current_valM1 < DOOR01_MAX:  # door01
            return "DOOR01"
        if DOOR02_MIN < current_valM1 < DOOR02_MAX:  # door02
            return "DOOR02"
        if DOOR03_MIN < current_valM1 < DOOR03_MAX:  # door03
            return "DOOR03"
        if DOOR04_MIN < current_valM1 < DOOR04_MAX:  # door04
            return "DOOR04"
        if DOOR05_MIN < current_valM1 < DOOR05_MAX:  # door05
            return "DOOR05"
        if DOOR06_MIN < current_valM1 < DOOR06_MAX:  # door06
            return "DOOR06"
        if DOOR07_MIN < current_valM1 < DOOR07_MAX:  # door07
            return "DOOR07"
        if DOOR08_MIN < current_valM1 < DOOR08_MAX:  # door08
            return "DOOR08"
        if DOOR09_MIN < current_valM1 < DOOR09_MAX:  # door09
            return "DOOR09"
        if DOOR10_MIN < current_valM1 < DOOR10_MAX:  # door10
            return "DOOR10"
        # if still nothing return, then must be some error
        return "ERROR"
