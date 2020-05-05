"""------------------------------------------------------------*-
  Main process for MISlocker
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019 - 2020
  version 2.00 - 28/03/2020
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import lcd
import button
import switches
from rfid import Gwiot_7304D2
from database import Database
import peripheral as pr
from datetime import datetime
import fingerPrint
import time
import buzzer as buz
import subprocess as subpro
from server import WebServer
import RPi.GPIO as GPIO  # default as BCM mode!
import signal
import os

# ---------------------------- Configurable parameters -------------------------
# -----Admin ID key:
ADMIN_KEY = '0x47106C'
TECHNICIAN_KEY = '0x531D1B'
PROMPT_WAITING_TIME = 7 # time the lock has to wait each time user open a door 
# INFO:
# lockerArray stores the rfid ID or fingerprint ID stand with locker that has been rented (maximum 20 locker)
# Index of LockerArray is also the number of the locker.
# Therefore, lockerArray has to omit index 0!!!
# 10 lockers
lockerArray = ["NULL", None, None, None, None, None, None, None, None, None, None]
# 20 lockers
# lockerArray = ["NULL", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
#                None, None, None, None, None]

NO_ID = 999999

SYS_MODE = False  # default mode is normal (use locker), turn true to turn to system mode (user can change their credentials)
last_second = 0   # for automatically return to locker mode
# --------------------------- Set Up ----------------------------------------
lcd.begin()
button.init()
switches.init()
rfid = Gwiot_7304D2()
dtb = Database()
pr.init()
fingerPrint.begin()
fingerPrint.activate()
server_pid = int()
server = WebServer()

# ==== ISR for cancel button when in server mode =========
def __cancelServerISR(channel):
    # global server_pid
    # global button
    os.kill(int(server.pid),signal.SIGTERM) #  find out the pid of the server and kill it
    # # incomplete member delete is handle
    button.reset()
    button.init()
    # server.shutdown()


def __wakeup_server():
    global server_pid
    
    # embedded a return way before open the server
    GPIO.setmode(GPIO.BCM)
    GPIO.remove_event_detect(button.CANCEL_BUTTON)
    GPIO.add_event_detect(button.CANCEL_BUTTON, GPIO.FALLING, callback=__cancelServerISR, bouncetime=button.DEBOUNCE*2)
    server_pid = server.pid
    # start server
    print('Server starting...')
    subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
    server.start()
    # while server.ON_FLAG:
    #     pass
    server.join() # Wait until the server thread terminates -- this is a function from the parent class Thread
    subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
    # in case user don't press cancel button, reset back button
    button.reset()
    button.init()


def __shortenName(name, limit):
    name_length = len(name)
    name += ' '
    if name_length <= limit:
        return name
    else:
        name_buffer = ""
        shorten_name = name[0]
        for i in range(1, name_length):
            if name[i] == ' ':
                shorten_name += '.'
                shorten_name += name[i + 1]
                name_buffer = ""  # not the last word, reset the buffer
            else:
                name_buffer += name[i + 1]
        shorten_name += name_buffer
        return shorten_name


def __dumpDebug(iid, name, mssv, rrfid, fing):
    print('member_id: ' + str(iid))
    print('Name: ' + str(name))
    print('MSSV: ' + str(mssv))
    print('RFID: ' + str(rrfid))
    print('fingerNumber: ' + str(fing))


def __openDoorProcedure(locker):
    pr.locker_nowBusy(locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
    pr.locker(locker, pr.OPEN)  # Open locker stand with this user id

    last_millis = datetime.now().second
    while switches.read() is "ALL_CLOSED":  # if the door is not open
        # then wait
        # wait for few seconds, if no signal then automatically use 'No' command
        # or if human push ok button
        if ((datetime.now().second - last_millis) > PROMPT_WAITING_TIME) or (button.read() is "BUT_OK"):
            break

    # now the door is open!
    time.sleep(0.5)  # wait for 0.5 second before proceeding for stablization
    pr.locker(locker, pr.CLOSE)  # close locker stand with this user id

    # clean rfid and finger buffer, if existed
    rfid.flush()  # flush out old buffer before get out
    fingerPrint.flush() # clear everthing before starting
    # save the last millis
    last_millis = datetime.now().second
    # --- ask user to close the door
    lcd.waitforDoorClose()
    # --- Detect if the door is open for too long
    while switches.read() is "OPEN":  # only get out if the door is close
        # wait for few seconds, if no signal then automatically use 'No' command
        if (datetime.now().second - last_millis) > PROMPT_WAITING_TIME*5:
            buz.beep(1)
            time.sleep(0.2)

        # ------------- admin priviledge -------------------- 
        if rfid.hasID():
            current_tag = rfid.tagID()
            if current_tag == ADMIN_KEY or current_tag == TECHNICIAN_KEY:
                # switches.clean()
                pr.locker(locker, pr.CLOSE)  # close locker stand with this user id
                button.clean()
                return
        # ---------------------------------------------------
        
        # if human push ok button, THIS IS FOR DEBUG ONLY!!! SHOULD DELETE WHEN IMPLEMENT TO REAL USECASE
        # if button.read() is "BUT_OK":
        #     pr.locker(locker, pr.CLOSE)  # close locker stand with this user id
        #     return
    # --- closed
    # depend on cases the red led will be open again or not
    button.clean()
    return


def __getNextAvailableLocker():
    if None in lockerArray:  # if still have vacancy
        next_locker_available = lockerArray.index(None)
        return next_locker_available
    else:  # no vacancy left
        return None


def __waitForConfirmation():
    # time.sleep(0.4)  # prevent debounce
    while True: # wait for someone to push OK button
        if button.read() == "BUT_OK": 
            return True
        if button.read() == "BUT_CANCEL":
            return False
        


def __showAdminInfo(current_locker):
    if lockerArray[current_locker] is None:  # no info
        print(lockerArray[current_locker])
        lcd.clear()
        lcd.infoLockerNoInfoPage(current_locker)
    else:  # info existed
        current_user = lockerArray[current_locker]
        if type(current_user) is int: # a real user 
            data = dtb.getMemberInfoByID(current_user) # with get user information with user_id
            user_name = data[2]
            user_mssv = data[3]
            lcd.clear()
            lcd.infoLockerPage(__shortenName(user_name,13), user_mssv, current_locker)
        else:  # temporary user with full rfid string
            lcd.clear()
            lcd.infoLockerTempPage(current_locker)


def __ChangeName(user_id):
    # Add personal information
    lcd.clear()
    lcd.confirmChangeInfo()

    # wait for confirm or cancel
    while True:
        button_state = button.read()
        if button_state == "BUT_OK": 
            break # continue to our program
        if button_state == "BUT_CANCEL":
            return # do not do anything
    

    # log old user name and mssv before replace with temporary one for not getting same mssv
    old_data = dtb.getMemberInfoByID(user_id)
    old_user_name = old_data[2]
    old_user_mssv = old_data[3]
    dtb.changeInfo(user_id, 'user name', 'B0000000') # dumb data for temporary
    
    # Create dumb user in the database
    dtb.addDumbUser()

    lcd.clear()
    lcd.changeNameMSSV()

    __wakeup_server()  # run collecting app

    # get info from server and then delete the incomplete user
    data = dtb.getLastMemberInfo() # incomplete user deleter already integrated - wake up server MUST go through this filter
    
    # below code are imune with incomplete user deleter, since it will have name and mssv
    user_valid = data[0]
    if user_valid:
        temp_user_id  = data[1]
        new_user_name = data[2]
        new_user_mssv = data[3]
        dtb.delMember(temp_user_id)
    else: # if user cancel in the middle of the logging, then return the old information
        new_user_name = old_user_name
        new_user_mssv = old_user_mssv
    
    # make change to the database
    dtb.changeInfo(user_id, new_user_name, new_user_mssv)

    # incomplete user due to cancelation of user is already delete above

    return


def __addRFID():
    lcd.clear()
    rfid.flush()  # clear everything before starting
    fingerPrint.flush() # clear everthing before starting
    while True:
        lcd.addRFIDPage()
        # wait for signal here
        if rfid.hasID():
            current_tag = rfid.tagID()
            [status, user_id] = dtb.addRFID(current_tag) # add rfid to database and return the user id from dtb
            if status:  # RFID added
                lcd.clear()
                lcd.addRFIDSuccessPage()
                __waitForConfirmation()
                return [True, user_id]
            else:  # RFID existed
                lcd.clear()
                lcd.addRFIDFailPage()
                choosing_pointer = 1  # default at first position
                lcd.pointerPos(2, choosing_pointer)
                # ------------------Button part ------------------
                while True:
                    status = button.read()
                    if status is "BUT_OK":
                        if choosing_pointer == 1:  # retry
                            lcd.clear()
                            rfid.flush()  # clear everything before starting
                            fingerPrint.flush() # clear everthing before starting
                            break
                        elif choosing_pointer == 2: # cancel
                            # clean rfid and finger buffer, if existed
                            rfid.flush()  # flush out old buffer before get out
                            fingerPrint.flush() # clear everthing before starting
                            return [False, NO_ID]
                        return [False, NO_ID]
                    elif status is "BUT_CANCEL":
                        # clean rfid and finger buffer, if existed
                        rfid.flush()  # flush out old buffer before get out
                        fingerPrint.flush() # clear everthing before starting
                        return [False, NO_ID]
                    elif status is "BUT_UP":
                        if choosing_pointer == 1:  # limit to 1
                            pass
                        else:
                            choosing_pointer -= 1
                        lcd.addRFIDFailPage()
                        lcd.pointerPos(2, choosing_pointer)
                    elif status is "BUT_DOWN":
                        if choosing_pointer == 2:  # limit to 2
                            pass
                        else:
                            choosing_pointer += 1
                        lcd.addRFIDFailPage()
                        lcd.pointerPos(2, choosing_pointer)

        # At anytime, if cancel was pressed, cancel the whole process
        if button.read() is "BUT_CANCEL":
            return [False, NO_ID]


def __ChangeRFID(user_id):
    lcd.clear()
    rfid.flush()  # clear everything before starting
    fingerPrint.flush() # clear everthing before starting
    while True:
        lcd.changeRFIDPage()
        # wait for signal here
        if rfid.hasID():
            current_tag = rfid.tagID()
            if dtb.searchRFID(current_tag)[0]:
                lcd.clear()
                lcd.changeRFIDExistedPage()
                __waitForConfirmation()
                return False
            else:
                status = dtb.changeRFID(user_id, current_tag) # add rfid to database and return the user id from dtb
                if status:  # RFID change successfully
                    lcd.clear()
                    lcd.changeRFIDSuccessPage()
                    __waitForConfirmation()
                    return True
                else:  # RFID failed to change
                    lcd.clear()
                    lcd.changeRFIDFailPage()
                    choosing_pointer = 1  # default at first position
                    lcd.pointerPos(2, choosing_pointer)
                    # ------------------Button part ------------------
                    while True:
                        status = button.read()
                        if status is "BUT_OK":
                            if choosing_pointer == 1:  # retry
                                lcd.clear()
                                rfid.flush()  # clear everything before starting
                                fingerPrint.flush() # clear everthing before starting
                                break
                            elif choosing_pointer == 2: # cancel
                                # clean rfid and finger buffer, if existed
                                rfid.flush()  # flush out old buffer before get out
                                fingerPrint.flush() # clear everthing before starting
                                return False
                            return False
                        elif status is "BUT_CANCEL":
                            # clean rfid and finger buffer, if existed
                            rfid.flush()  # flush out old buffer before get out
                            fingerPrint.flush() # clear everthing before starting
                            return False
                        elif status is "BUT_UP":
                            if choosing_pointer == 1:  # limit to 1
                                pass
                            else:
                                choosing_pointer -= 1
                            lcd.changeRFIDFailPage()
                            lcd.pointerPos(2, choosing_pointer)
                        elif status is "BUT_DOWN":
                            if choosing_pointer == 2:  # limit to 2
                                pass
                            else:
                                choosing_pointer += 1
                            lcd.changeRFIDFailPage()
                            lcd.pointerPos(2, choosing_pointer)

        # At anytime, if cancel was pressed, cancel the whole process
        if button.read() is "BUT_CANCEL":
            return False


def __addFingerPrint(status_rfid, user_id):
    if status_rfid: # if rfid was added successfully, then save the fingerPrint to the same user_id
        lcd.clear()
        # IN NORMAL OPERATION, THIS FUNCTION INTENDED TO GO THROUGH WHILE LOOP ONLY ONCE
        while True: # NOT AN USUAL INFINITY LOOP, it existed for the sake of adding fingerPrint fail
            lcd.addFingerPage01()
            [status, position_number] = fingerPrint.first_enroll() # this function return ["DONE",0]
            if status == "CANCEL":
                fingerPrint.flush() # clear everthing before starting
                return # someone press cancel button, so cancel the process
            if status == "EXISTED":
                lcd.clear()
                lcd.addFingerExistedPage()
                __waitForConfirmation()
                fingerPrint.flush() # clear everthing before starting
                return
            if status == "DONE": # first enroll success
                lcd.clear()
                lcd.addFingerPage02()
                time.sleep(1.5)
                lcd.clear()
                lcd.addFingerPage03()
                [status, position_number] = fingerPrint.second_enroll() # this function return ["DONE", positionNumber]
                if status == "CANCEL":
                    fingerPrint.flush() # clear everthing before starting
                    return # someone press cancel button, so cancel the process
                if status == "DONE": # second enroll success
                    status_2 = dtb.addFinger(user_id, position_number) # add fingerPrint to database and return the user id from dtb
                    if status_2:  # fingerPrint added to database
                        lcd.clear()
                        lcd.addFingerSuccessPage()
                        __waitForConfirmation()
                        fingerPrint.flush() # clear everthing before starting
                        return
                    else:  # fingerPrint failed to add to database
                        print('fingerPrint failed to add to database') # for debug
                        lcd.clear()
                        lcd.addFingerFailPage()
                        choosing_pointer = 1  # default at first position
                        lcd.pointerPos(2, choosing_pointer)
                        # ------------------Button part ------------------
                        while True:
                            status = button.read()
                            if status is "BUT_OK":
                                if choosing_pointer == 1:  # retry
                                    lcd.clear()
                                    break # try adding again
                                # all other option equal to cancel
                                fingerPrint.flush() # clear everthing before starting
                                return  # return the optional fingerPrint adding function
                            elif status is "BUT_CANCEL":
                                fingerPrint.flush() # clear everthing before starting
                                return  # return the optional fingerPrint adding function
                            elif status is "BUT_UP":
                                if choosing_pointer == 1:  # limit to 1
                                    pass
                                else:
                                    choosing_pointer -= 1
                                    lcd.addFingerFailPage()
                                    lcd.pointerPos(2, choosing_pointer)
                            elif status is "BUT_DOWN":
                                if choosing_pointer == 2:  # limit to 2
                                    pass
                                else:
                                    choosing_pointer += 1
                                    lcd.addFingerFailPage()
                                    lcd.pointerPos(2, choosing_pointer)
                else:  # second enroll failed
                    print('second enroll failed') # for debug
                    print(status) # for debug
                    lcd.clear()
                    lcd.addFingerFailPage()
                    choosing_pointer = 1  # default at first position
                    lcd.pointerPos(2, choosing_pointer)
                    # ------------------Button part ------------------
                    while True:
                        status = button.read()
                        if status is "BUT_OK":
                            if choosing_pointer == 1:  # retry
                                lcd.clear()
                                break # try adding again
                            # all other option equal to cancel
                            fingerPrint.flush() # clear everthing before starting
                            return  # return the optional fingerPrint adding function
                        elif status is "BUT_CANCEL":
                            fingerPrint.flush() # clear everthing before starting
                            return  # return the optional fingerPrint adding function
                        elif status is "BUT_UP":
                            if choosing_pointer == 1:  # limit to 1
                                pass
                            else:
                                choosing_pointer -= 1
                                lcd.addFingerFailPage()
                                lcd.pointerPos(2, choosing_pointer)
                        elif status is "BUT_DOWN":
                            if choosing_pointer == 2:  # limit to 2
                                pass
                            else:
                                choosing_pointer += 1
                                lcd.addFingerFailPage()
                                lcd.pointerPos(2, choosing_pointer)
            else:  # first enroll failed
                print('first enroll failed') # for debug
                print(status) # for debug
                lcd.clear()
                lcd.addFingerFailPage()
                choosing_pointer = 1  # default at first position
                lcd.pointerPos(2, choosing_pointer)
                # ------------------Button part ------------------
                while True:
                    status = button.read()
                    if status is "BUT_OK":
                        if choosing_pointer == 1:  # retry
                            lcd.clear()
                            break # try adding again
                        # all other option equal to cancel
                        fingerPrint.flush() # clear everthing before starting
                        return  # return the optional fingerPrint adding function
                    elif status is "BUT_CANCEL":
                        fingerPrint.flush() # clear everthing before starting
                        return  # return the optional fingerPrint adding function
                    elif status is "BUT_UP":
                        if choosing_pointer == 1:  # limit to 1
                            pass
                        else:
                            choosing_pointer -= 1
                            lcd.addFingerFailPage()
                            lcd.pointerPos(2, choosing_pointer)
                    elif status is "BUT_DOWN":
                        if choosing_pointer == 2:  # limit to 2
                            pass
                        else:
                            choosing_pointer += 1
                            lcd.addFingerFailPage()
                            lcd.pointerPos(2, choosing_pointer)    
    else: # rfid was not added successfully
        fingerPrint.flush() # clear everthing before starting
        return  # let other function take care


def __ChangeFinger(user_id):
    lcd.clear()
    # IN NORMAL OPERATION, THIS FUNCTION INTENDED TO GO THROUGH WHILE LOOP ONLY ONCE
    while True: # NOT AN USUAL INFINITY LOOP, it existed for the sake of adding fingerPrint fail
        lcd.changeFingerPage01()
        [status, position_number] = fingerPrint.first_enroll() # this function return ["DONE",0]
        if status == "CANCEL":
            fingerPrint.flush() # clear everthing before starting
            return # someone press cancel button, so cancel the process
        if status == "EXISTED":
            lcd.clear()
            lcd.changeFingerExistedPage()
            __waitForConfirmation()
            fingerPrint.flush() # clear everthing before starting
            return
        if status == "DONE": # first enroll success
            lcd.clear()
            lcd.changeFingerPage02()
            time.sleep(1.5)
            lcd.clear()
            lcd.changeFingerPage03()
            [status, position_number] = fingerPrint.second_enroll() # this function return ["DONE", positionNumber]
            if status == "CANCEL":
                fingerPrint.flush() # clear everthing before starting
                return # someone press cancel button, so cancel the process
            if status == "DONE": # second enroll success
                old_pattern = dtb.getMemberInfoByID(user_id)[5]  # get old fingerprint pattern out
                fingerPrint.delete(old_pattern)  # delete it
                status_2 = dtb.changeFinger(user_id, position_number)  # add fingerPrint to database and return the user id from dtb
                if status_2:  # fingerPrint added to database
                    lcd.clear()
                    lcd.changeFingerSuccessPage()
                    __waitForConfirmation()
                    fingerPrint.flush() # clear everthing before getout
                    return
                else:  # fingerPrint failed to change in database
                    print('fingerPrint failed to change in database') # for debug
                    lcd.clear()
                    lcd.changeFingerFailPage()
                    choosing_pointer = 1  # default at first position
                    lcd.pointerPos(2, choosing_pointer)
                    # ------------------Button part ------------------
                    while True:
                        status = button.read()
                        if status is "BUT_OK":
                            if choosing_pointer == 1:  # retry
                                lcd.clear()
                                break # try adding again
                            # all other option equal to cancel
                            fingerPrint.flush() # clear everthing before starting
                            return  # return the optional fingerPrint adding function
                        elif status is "BUT_CANCEL":
                            fingerPrint.flush() # clear everthing before starting
                            return  # return the optional fingerPrint adding function
                        elif status is "BUT_UP":
                            if choosing_pointer == 1:  # limit to 1
                                pass
                            else:
                                choosing_pointer -= 1
                                lcd.changeFingerFailPage()
                                lcd.pointerPos(2, choosing_pointer)
                        elif status is "BUT_DOWN":
                            if choosing_pointer == 2:  # limit to 2
                                pass
                            else:
                                choosing_pointer += 1
                                lcd.changeFingerFailPage()
                                lcd.pointerPos(2, choosing_pointer)
            else:  # second enroll failed
                print('second enroll failed') # for debug
                print(status) # for debug
                lcd.clear()
                lcd.changeFingerFailPage()
                choosing_pointer = 1  # default at first position
                lcd.pointerPos(2, choosing_pointer)
                # ------------------Button part ------------------
                while True:
                    status = button.read()
                    if status is "BUT_OK":
                        if choosing_pointer == 1:  # retry
                            lcd.clear()
                            break # try adding again
                        # all other option equal to cancel
                        fingerPrint.flush() # clear everthing before starting
                        return  # return the optional fingerPrint adding function
                    elif status is "BUT_CANCEL":
                        fingerPrint.flush() # clear everthing before starting
                        return  # return the optional fingerPrint adding function
                    elif status is "BUT_UP":
                        if choosing_pointer == 1:  # limit to 1
                            pass
                        else:
                            choosing_pointer -= 1
                            lcd.changeFingerFailPage()
                            lcd.pointerPos(2, choosing_pointer)
                    elif status is "BUT_DOWN":
                        if choosing_pointer == 2:  # limit to 2
                            pass
                        else:
                            choosing_pointer += 1
                            lcd.changeFingerFailPage()
                            lcd.pointerPos(2, choosing_pointer)
        else:  # first enroll failed
            print('first enroll failed') # for debug
            print(status) # for debug
            lcd.clear()
            lcd.changeFingerFailPage()
            choosing_pointer = 1  # default at first position
            lcd.pointerPos(2, choosing_pointer)
            # ------------------Button part ------------------
            while True:
                status = button.read()
                if status is "BUT_OK":
                    if choosing_pointer == 1:  # retry
                        lcd.clear()
                        break # try adding again
                    # all other option equal to cancel
                    fingerPrint.flush() # clear everthing before starting
                    return  # return the optional fingerPrint adding function
                elif status is "BUT_CANCEL":
                    fingerPrint.flush() # clear everthing before starting
                    return  # return the optional fingerPrint adding function
                elif status is "BUT_UP":
                    if choosing_pointer == 1:  # limit to 1
                        pass
                    else:
                        choosing_pointer -= 1
                        lcd.changeFingerFailPage()
                        lcd.pointerPos(2, choosing_pointer)
                elif status is "BUT_DOWN":
                    if choosing_pointer == 2:  # limit to 2
                        pass
                    else:
                        choosing_pointer += 1
                        lcd.changeFingerFailPage()
                        lcd.pointerPos(2, choosing_pointer)


def __oneTimeUserCase(current_tag):
    current_locker = __getNextAvailableLocker()
    if current_locker is None:  # out of vacancy
        lcd.clear()
        lcd.outOfVacancyPage()

        __waitForConfirmation()

        lcd.clear()
        rfid.flush()  # flush out old buffer before get out
        fingerPrint.flush() # clear everthing before get out
        return
    else:  # new locker available
        lcd.clear()
        lcd.welcomeTempPage(current_locker)
        lockerArray[current_locker] = current_tag
        __openDoorProcedure(current_locker) # this function open the locker and wait the user to close it

        pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

        lcd.clear()
        rfid.flush()  # flush out old buffer before get out
        fingerPrint.flush() # clear everthing before get out
        return


def __oneTimeUser_returnCase(current_tag):
    current_locker = lockerArray.index(current_tag)  # get the locker out
    lcd.clear()
    lcd.returnTempPage(current_locker)
    __openDoorProcedure(current_locker) # this function open the locker and wait the user to close it
    lockerArray[current_locker] = None

    lcd.clear()
    rfid.flush()  # flush out old buffer before get out
    fingerPrint.flush() # clear everthing before get out
    return


def __addNewIDCase():
    user_id = NO_ID  # create user id
    # add RFID
    [status_rfid, user_id_rfid] = __addRFID()
    # now time to add fingerPrint (optional)
    __addFingerPrint(status_rfid, user_id_rfid)

    if status_rfid :  # rfid availables is mandatory
        user_id = user_id_rfid

        if user_id == NO_ID:
            raise Exception("Error with database, please check again")

        # Add personal information
        lcd.clear()
        lcd.addNewInfo()
        __wakeup_server()  # run collecting app

        data = dtb.getLastMemberInfo() # incomplete user deleter already integrated - wake up server MUST go through this filter
        user_valid = data[0]

        if user_valid:
            user_id = data[1]
            [got_data, userID, user_name, user_mssv, user_rfid, user_fing] = dtb.getMemberInfoByID(user_id)
            userCase(got_data, userID, user_name, user_mssv, user_rfid, user_fing)
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out
            return # return to No Info menu

     # no rfid is available or user is invalid
    lcd.clear()
    lcd.cancelNewUserPage()
    time.sleep(1.5)
    rfid.flush()  # flush out old buffer before get out
    fingerPrint.flush() # clear everthing before get out
    return  # return to No Info menu


def userCase(got_data, user_id, user_name, user_mssv, user_rfid, user_fing):
    global lockerArray
    if got_data:  # if get info from database successfully
        # ------------  OLD LOCKER!!! -----------------
        if user_id in lockerArray:  # if user is renting a locker
            current_locker = lockerArray.index(user_id)
            lcd.clear()
            lcd.returnPage(__shortenName(user_name,13), current_locker)  # Name, locker_num
            lockerArray[current_locker] = user_id
            __openDoorProcedure(current_locker) # this function open the locker and wait the user to close it

            pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

            __dumpDebug(user_id, user_name, user_mssv, user_rfid, user_fing)

            # --- ask user if they want to continue using the locker
            choosing_pointer = 1  # equivalent to Yes
            lcd.clear()
            lcd.questionPage()
            lcd.pointerPos(2, choosing_pointer)  # option, pointer
            last_millis = datetime.now().second
            while True:
                status = button.read()
                if status is "BUT_OK":
                    if choosing_pointer == 2:  # 'No' command
                        lockerArray[current_locker] = None  # clear info in this locker
                        pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
                        lcd.clear()
                        rfid.flush()  # flush out old buffer before get out
                        fingerPrint.flush() # clear everthing before get out
                        return  # return to waiting state
                    elif choosing_pointer == 1:  # 'Yes' command
                        lcd.clear()
                        lcd.continueUsingPage()
                        time.sleep(2)
                        lcd.clear()
                        rfid.flush()  # flush out old buffer before get out
                        fingerPrint.flush() # clear everthing before get out
                        return  # return to waiting state
                elif status is "BUT_CANCEL":
                    lockerArray[current_locker] = None  # clear info in this locker
                    pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
                    lcd.clear()
                    # clean rfid and finger buffer, if existed
                    rfid.flush()  # flush out old buffer before get out
                    fingerPrint.flush() # clear everthing before get out
                    return  # return to waiting state
                elif status is "BUT_UP":
                    if choosing_pointer == 1:  # limit to 1
                        pass
                    else:
                        choosing_pointer -= 1
                    lcd.questionPage()
                    lcd.pointerPos(2, choosing_pointer)  # option, pointer
                elif status is "BUT_DOWN":
                    if choosing_pointer == 2:  # limit to 2
                        pass
                    else:
                        choosing_pointer += 1
                    lcd.questionPage()
                    lcd.pointerPos(2, choosing_pointer)  # option, pointer

                # wait for few seconds, if no signal then automatically use 'No' command
                if (datetime.now().second - last_millis) > PROMPT_WAITING_TIME/2:
                    lockerArray[current_locker] = None  # clear info in this locker
                    pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
                    lcd.clear()
                    rfid.flush()  # flush out old buffer before get out
                    fingerPrint.flush() # clear everthing before get out
                    return  # return to waiting state
        # ------------  NEW LOCKER!!! -----------------
        else:  # if this user don't have any locker yet
            current_locker = __getNextAvailableLocker()
            if current_locker is None:  # out of vacancy
                lcd.clear()
                lcd.outOfVacancy()

                __waitForConfirmation()

                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
            else:  # new locker available
                lcd.clear()
                lcd.welcomePage(__shortenName(user_name,13), user_mssv, current_locker)  # Name, mssv, locker_num
                lockerArray[current_locker] = user_id
                __openDoorProcedure(current_locker) # this function open the locker and wait the user to close it

                pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

                __dumpDebug(user_id, user_name, user_mssv, user_rfid, user_fing)

                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
    else:
        print('cannot get info from database with this user-database-id')
        lcd.clear()
        rfid.flush()  # flush out old buffer before get out
        fingerPrint.flush() # clear everthing before get out
        return


def changeDataCase(user_id, user_name):
    lcd.clear()
    lcd.changeInfoPage(__shortenName(user_name,13))
    choosing_pointer = 1  # default at first position
    lcd.pointerPos(3, choosing_pointer)
    last_millis = datetime.now().second
    while True:
        status = button.read()
        if status is "BUT_OK":
            if choosing_pointer == 1:  # Change name/MSSV
                __ChangeName(user_id)
                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
            elif choosing_pointer == 2:  # Change RFID
                __ChangeRFID(user_id)
                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
            elif choosing_pointer == 3:  # Change Fingerprint
                __ChangeFinger(user_id)
                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
        elif status is "BUT_CANCEL":
            lcd.clear()
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out
            return  # return to waiting state
        elif status is "BUT_UP":
            if choosing_pointer == 1:  # limit to 1
                pass
            else:
                choosing_pointer -= 1
            lcd.changeInfoPage(__shortenName(user_name,13))
            lcd.pointerPos(3, choosing_pointer)  # option, pointer
        elif status is "BUT_DOWN":
            if choosing_pointer == 3:  # limit to 3
                pass
            else:
                choosing_pointer += 1
            lcd.changeInfoPage(__shortenName(user_name,13))
            lcd.pointerPos(3, choosing_pointer)  # option, pointer

        # wait for few seconds, if no signal then automatically use 'No' command
        if (datetime.now().second - last_millis) > PROMPT_WAITING_TIME*3:
            lcd.clear()
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out
            return  # return to waiting state


def adminCase():
    choosing_pointer = 1  # default at first position
    lcd.clear()
    lcd.mainAdminPage()
    lcd.pointerPos(3, choosing_pointer)
    while True:
        status = button.read()
        if status is "BUT_OK":
            # //////////////// DELETE ALL DATABASE /////////////////
            if choosing_pointer == 3:  # Delete All database command
                lcd.clear()
                lcd.warningDeletePage()

                # press OK button
                if __waitForConfirmation(): # wait loop integrated inside

                    dtb.delAllMember() # delete all member in the database
                    fingerPrint.deleteAll() # delete all fingerprint pattern in fingerprint sensor database
                    
                    lcd.clear()
                    lcd.DBdeleteDonePage()
                    time.sleep(2)
                
                lcd.clear()
                lcd.mainAdminPage()
                lcd.pointerPos(3, choosing_pointer)
                
            # //////////////// MODIFY DATABASE /////////////////
            if choosing_pointer == 2:  # Modify database command
                lcd.clear()
                lcd.modifyDatabaseInfoPage()

                __waitForConfirmation()

                lcd.clear()
                lcd.mainAdminPage()
                lcd.pointerPos(3, choosing_pointer)

            # //////////////// LOCKER INFO ///////////////////
            elif choosing_pointer == 1:  # Locker info command
                global lockerArray
                current_locker = 1
                __showAdminInfo(current_locker)
                time.sleep(0.5)  # stabilize time
                # ------------------Button part ------------------
                while True:
                    status = button.read()
                    if status is "BUT_OK":
                        lcd.clear()
                        lcd.unlockConfirmPage(current_locker)
                        lockerArray[current_locker] = None # clear buffer
                        __openDoorProcedure(current_locker) # this function open the locker and wait the user to close it
                        __showAdminInfo(current_locker)
                    elif status is "BUT_CANCEL":
                        rfid.flush()  # flush out old buffer before get out
                        fingerPrint.flush() # clear everthing before get out
                        break  # return to main menu
                    elif status is "BUT_UP":
                        if current_locker == (len(lockerArray)-1):  # if reached the limit of lockers
                            pass
                        else:
                            current_locker += 1
                            __showAdminInfo(current_locker)
                    elif status is "BUT_DOWN":
                        if current_locker == 1:  # limit to 1
                            pass
                        else:
                            current_locker -= 1
                            __showAdminInfo(current_locker)
                lcd.clear()
                lcd.mainAdminPage()
                lcd.pointerPos(3, choosing_pointer)  # choosing_pointer = 2 since the last time

        elif status is "BUT_CANCEL":
            lcd.clear()
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out
            return  # return to waiting state
        elif status is "BUT_UP":
            if choosing_pointer == 1:  # limit to 1
                pass
            else:
                choosing_pointer -= 1
            lcd.mainAdminPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer
        elif status is "BUT_DOWN":
            if choosing_pointer == 3:  # limit to 3
                pass
            else:
                choosing_pointer += 1
            lcd.mainAdminPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer
    # end while loop


def noInfoCase(current_tag):
    lcd.clear()
    lcd.unknownIDPage()
    choosing_pointer = 1  # default at first position
    lcd.pointerPos(3, choosing_pointer)
    last_millis = datetime.now().second
    while True:
        status = button.read()
        if status is "BUT_OK":
            if choosing_pointer == 2:  # One-time user command
                __oneTimeUserCase(current_tag)
                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
            elif choosing_pointer == 1:  # Add new ID command
                __addNewIDCase()
                lcd.clear()
                rfid.flush()  # flush out old buffer before get out
                fingerPrint.flush() # clear everthing before get out
                return
        elif status is "BUT_CANCEL":
            lcd.clear()
            # clean rfid and finger buffer, if existed
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out
            return  # return to waiting state
        elif status is "BUT_UP":
            if choosing_pointer == 1:  # limit to 1
                pass
            else:
                choosing_pointer -= 1
            lcd.unknownIDPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer
        elif status is "BUT_DOWN":
            if choosing_pointer == 2:  # limit to 2
                pass
            else:
                choosing_pointer += 1
            lcd.unknownIDPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer

        # wait for few seconds, if no signal then automatically use 'No' command
        if (datetime.now().second - last_millis) > PROMPT_WAITING_TIME*3:
            lcd.clear()
            # clean rfid and finger buffer, if existed
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out
            return  # return to waiting state


def main():  # Main program block
    # ---------------------------- Setup ----------------------------------------
    lcd.clear()
    global SYS_MODE
    print('number of member in database: ', dtb.number_of_member())
    print("System ready!")
    # ---------------------------- Loop -----------------------------------------
    while True:
        if SYS_MODE:  # system mode for user --> change personal info, rfid, fingerprint
            lcd.waitPage_system()
        else:         # normal mode for user --> use locker 
            lcd.waitPage_normal()

        # ================== RFID case ==================
        if rfid.hasID():
            current_tag = rfid.tagID()
            [id_existed, userID] = dtb.searchRFID(current_tag)
            if id_existed:  # if existed this ID --> User
                [got_data, user_id, user_name, user_mssv, user_rfid, user_fing] = dtb.getMemberInfoByID(userID)
                if (user_name or user_mssv) is None:  # if we have unfinished data
                    dtb.delMember(user_id) # delete it from database
                    buz.beep(1)  # sound notification
                    print('RFID not found!')
                    noInfoCase(current_tag)  # turn user to no info case
                else: # data is all good and ready to be used
                    if SYS_MODE:  # system mode for user --> change personal info, rfid, fingerprint
                        changeDataCase(user_id, user_name)
                    else:         # normal mode for user --> use locker 
                        userCase(got_data, user_id, user_name, user_mssv, user_rfid, user_fing)
            else:  # this ID is not existed in the user database
                if current_tag in lockerArray:  # return case for temporary user
                    __oneTimeUser_returnCase(current_tag)
                elif current_tag == ADMIN_KEY or current_tag == TECHNICIAN_KEY:
                    adminCase()
                else:
                    buz.beep(1)  # sound notification
                    print('RFID not found!')
                    if SYS_MODE:  # system mode for user --> change personal info, rfid, fingerprint
                        noInfoCase(current_tag)  # user have no info yet
                    else:         # normal mode for user --> only use locker 
                        __oneTimeUserCase(current_tag)
                        lcd.clear()
            rfid.flush()  # flush out old buffer before get out
            fingerPrint.flush() # clear everthing before get out

        # ================== FingerPrint case ==================
        status_fingerprint = fingerPrint.check()
        if status_fingerprint == "NO DATA":
            pass  # if no data found, then do nothing
        elif status_fingerprint == "MATCHED":
            current_fingerprint = fingerPrint.user_position()  # save current fingerprint position to a variable
            [id_existed, userID] = dtb.searchFinger(current_fingerprint)
            if id_existed:  # if existed this ID --> User
                [got_data, user_id, user_name, user_mssv, user_rfid, user_fing] = dtb.getMemberInfoByID(userID)
                if (user_name or user_mssv) is None:  # if we have unfinished data
                    dtb.delMember(user_id) # delete it from database
                    fingerPrint.delete(current_fingerprint)  # delete fingerprint pattern in the dtb of the fingerprint sensor
                    buz.beep(2)  # sound notification of declining to proceed
                else: # data is all good and ready to be used
                    if SYS_MODE:  # system mode for user --> change personal info, rfid, fingerprint
                        changeDataCase(user_id, user_name)
                    else:         # normal mode for user --> use locker 
                        userCase(got_data, user_id, user_name, user_mssv, user_rfid, user_fing)
            else:  # this ID is not existed in the user database
                fingerPrint.delete(current_fingerprint)  # delete fingerprint pattern in the dtb of the fingerprint sensor
                buz.beep(2)  # sound notification of declining to proceed
        else:  # if current pattern is not found in the database
            buz.beep(2)  # sound notification of declining to proceed
        
        # ================== Mode changing ==================
        sys_command = button.read()
        if sys_command is "BUT_DOWN":
            SYS_MODE = True
            global last_second
            last_second = datetime.now().second
        if sys_command is "BUT_UP" or (datetime.now().second - last_second) > PROMPT_WAITING_TIME*3:
            SYS_MODE = False


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit) as e:
        print(e)
        # turn on ro
        subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False)
        subpro.call(['sudo','mount','-o','remount,ro','/boot'], shell=False)
        
        subpro.Popen(['python3','syshalt.py'], shell=False) # closing procedure, included close off peripherals
        rfid.stop()  # REMEMBER TO DO THIS SINCE THE READING IN C DON'T EXIT BY ITSELF!

    except (OSError, Exception) as e: # I/O error or exception
        print(e)
        # turn on ro
        subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False)
        subpro.call(['sudo','mount','-o','remount,ro','/boot'], shell=False)
        
        lcd.systemErrorPage()
        pr.init()    # clear all locks and LEDs before shutdown
        rfid.stop()  # REMEMBER TO DO THIS SINCE THE READING IN C DON'T EXIT BY ITSELF!
    