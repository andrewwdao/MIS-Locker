import button
import switch
import time

button.init()
switch.init()


while True:
    
    button_state = button.read()
    switch_state = switch.read()

    if(button_state=="BUT_OK"):
        print("Hello world OK")

    if(button_state=="BUT_CANCEL"):
        print("Hello world CANCEL")

    if(button_state=="BUT_UP"):
        print("Hello world UP")
    
    if(button_state=="BUT_DOWN"):
        print("Hello world DOWN")
    
    if(switch_state=="M1_OPEN"):
        print("Hello world M1 OPEN")
    
    if(button_state=="M2_OPEN"):
        print("Hello world M2 OPEN")
