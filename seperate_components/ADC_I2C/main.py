import button
import time

button.init()

# switches = adc_switches()
while True:
    # print(switches.readRawM1())
    #print(switches.read())
    if(button.read()=="BUT_OK"):
        print("Hello world")
    #print(button.read())
    # time.sleep(1)