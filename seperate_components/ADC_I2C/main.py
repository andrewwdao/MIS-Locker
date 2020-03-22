from adc import adc_button,adc_switches
import time
button = adc_button()
switches = adc_switches()
while True:
    print(switches.readRawM1())
    # print(button.readRaw())
    #print(switches.read())
    time.sleep(1)