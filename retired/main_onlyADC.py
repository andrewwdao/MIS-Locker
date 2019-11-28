from adc import adc_button, adc_switches
import time

button = adc_button()
switches = adc_switches()
while True:
    # print(button.readRaw())
    # print(switches.read())
    print(button.readRaw())
    time.sleep(0.3)
