from adc import adc_button,adc_switches
import time
button = adc_button()
switches = adc_switches()
while True:
    # print(button.read())
    print(switches.read())
    time.sleep(0.5)