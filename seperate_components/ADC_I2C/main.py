import button
import time

button.init()

# switches = adc_switches()
while True:
    # print(switches.readRawM1())
    #print(switches.read())
    button_state = button.read()
    if(button_state=="BUT_OK"):
        print("Hello world OK")

    if(button_state=="BUT_CANCEL"):
        print("Hello world CANCEL")

    if(button_state=="BUT_UP"):
        print("Hello world UP")
    
    if(button_state=="BUT_DOWN"):
        print("Hello world DOWN")
    #print(button.read())
    # time.sleep(1)