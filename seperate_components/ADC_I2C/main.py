import button
import switches
import time

button.init()
switches.init()


while True:
    
    button_state = button.read()
    switch_state = switches.read()

    if(button_state=="BUT_OK"):
        print("Hello world OK")

    if(button_state=="BUT_CANCEL"):
        print("Hello world CANCEL")

    if(button_state=="BUT_UP"):
        print("Hello world UP")
    
    if(button_state=="BUT_DOWN"):
        print("Hello world DOWN")
    
    if(switch_state=="OPEN"):
        print("Hello world M1 OPEN")
