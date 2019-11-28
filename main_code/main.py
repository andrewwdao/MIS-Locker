import lcd
from adc import adc_button, adc_switches
from rfid import RDM6300
from database import Database
import peripheral as pr
from datetime import datetime, timezone

import time

# ---------------------------- Configurable parameters -------------------------
# -----Admin ID key:
ADMIN_KEY = '810093B8D6\r\n'
PROMPT_WAITING_TIME = 8
TEMPORARY_USER_ID = 9999
DOOR = (
    "NULL",
    "DOOR01",
    "DOOR02",
    "DOOR03",
    "DOOR04",
    "DOOR05",
    "DOOR06",
    "DOOR07",
    "DOOR08",
    "DOOR09",
    "DOOR10",
    "DOOR11",
    "DOOR12",
    "DOOR13",
    "DOOR14",
    "DOOR15",
    "DOOR16",
    "DOOR17",
    "DOOR18",
    "DOOR19",
    "DOOR20"
)
# --------------------------- Set Up ----------------------------------------
lcd.begin()
button = adc_button()
switches = adc_switches()
rfid = RDM6300('/dev/ttyUSB0', 115200)
dtb = Database()
pr.init()
next_locker_available = 1  # next available locker (default at 1)
# database id stand with locker that has been rented (20 locker)
# omit index 0!!!
lockerArray = [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
               None, None, None, None, None]


def dumpDebug(iid, name, mssv, rrfid, fing):
    print('member_id: ' + str(iid))
    print('Name: ' + str(name))
    print('MSSV: ' + str(mssv))
    print('RFID: ' + str(rrfid))
    print('fingerNumber: ' + str(fing))


def userCase(userID):
    global lockerArray
    data = dtb.getInfo(userID)
    [got_data, user_id, user_name, user_mssv, user_rfid, user_fing] = data

    if got_data:  # if get info from database successfully
        # ------------  OLD LOCKER!!! -----------------
        if user_id in lockerArray:  # if user is renting a locker
            current_locker = lockerArray.index(user_id)
            lcd.clear()
            lcd.returnPage(user_name, current_locker)  # Name, locker_num

            pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
            pr.locker(current_locker, pr.OPEN)  # Open locker stand with this user id
            lockerArray[current_locker] = user_id

            dumpDebug(user_id, user_name, user_mssv, user_rfid, user_fing)

            last_millis = datetime.now(timezone.utc)
            while switches.read() is not DOOR[current_locker]:  # if the door is not open
                # then wait
                # wait for 10 seconds, if no signal then automatically use 'No' command
                if (datetime.now(timezone.utc) - last_millis).seconds > PROMPT_WAITING_TIME:
                    break
            # now the door is open!
            time.sleep(2)  # wait for 2 second before proceeding
            pr.locker(current_locker, pr.CLOSE)  # close locker stand with this user id

            # --- wait for the locker is closed
            while switches.read() is not "ALL_CLOSED":  # wait for the locker to be closed
                # wait and print something to debug!
                print(switches.read())
            # --- closed

            pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

            choosing_pointer = 2  # equivalent to No
            lcd.clear()
            lcd.questionPage()
            lcd.pointerPos(2, choosing_pointer)  # option, pointer
            last_millis = datetime.now(timezone.utc)
            while True:
                status = button.read()
                if status is "BUT_OK":
                    if choosing_pointer == 2:  # 'No' command
                        lockerArray[current_locker] = None  # clear info in this locker
                        pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
                        lcd.clear()
                        return  # return to waiting state
                    elif choosing_pointer == 1:  # 'Yes' command
                        lcd.clear()
                        lcd.continueUsingPage()
                        time.sleep(3)
                        lcd.clear()
                        return  # return to waiting state
                elif status is "BUT_CANCEL":
                    lockerArray[current_locker] = None  # clear info in this locker
                    pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
                    lcd.clear()
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

                # wait for 10 seconds, if no signal then automatically use 'No' command
                if (datetime.now(timezone.utc) - last_millis).seconds > PROMPT_WAITING_TIME:
                    lockerArray[current_locker] = None  # clear info in this locker
                    pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
                    lcd.clear()
                    return  # return to waiting state
        # ------------  NEW LOCKER!!! -----------------
        else:  # if this user don't have any locker yet
            global next_locker_available
            current_locker = next_locker_available
            if None in lockerArray:  # if still have vacancy
                next_locker_available = lockerArray.index(None)  # automatically set to the lowest locker available
            lcd.clear()
            lcd.welcomePage(user_name, user_mssv, current_locker)  # Name, mssv, locker_num

            pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
            pr.locker(current_locker, pr.OPEN)
            lockerArray[current_locker] = user_id

            dumpDebug(user_id, user_name, user_mssv, user_rfid, user_fing)

            last_millis = datetime.now(timezone.utc)
            while switches.read() is not DOOR[current_locker]:  # if the door is not open
                # then wait
                # wait for 10 seconds, if no signal then automatically use 'No' command
                if (datetime.now(timezone.utc) - last_millis).seconds > PROMPT_WAITING_TIME:
                    break
            # now the door is open!
            time.sleep(2)  # wait for 2 second before proceeding
            pr.locker(current_locker, pr.CLOSE)  # close locker stand with this user id

            # --- wait for the locker is closed
            while switches.read() is not "ALL_CLOSED":  # wait for the locker to be closed
                print(switches.read())
            # --- closed

            pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

            lcd.clear()
            return
    else:
        print('cannot get info from database with this user-database-id')
        lcd.clear()
        return


def adminCase():
    choosing_pointer = 1  # default at first position
    lcd.clear()
    lcd.mainAdminPage()
    lcd.pointerPos(3, choosing_pointer)
    while True:
        status = button.read()
        if status is "BUT_OK":
            if choosing_pointer == 1:  # Modify database command
                lcd.clear()
                lcd.modifyDatabaseInfoPage()

                while button.read() is "BUT_NO_PRESS":
                    # wait for someone to push any button
                    pass

                lcd.clear()
                lcd.mainAdminPage()
                lcd.pointerPos(3, choosing_pointer)

            elif choosing_pointer == 2:  # Locker info command
                lockerInfo()

        elif status is "BUT_CANCEL":
            lcd.clear()
            return  # return to waiting state
        elif status is "BUT_UP":
            if choosing_pointer == 1:  # limit to 1
                pass
            else:
                choosing_pointer -= 1
            lcd.mainAdminPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer
        elif status is "BUT_DOWN":
            if choosing_pointer == 2:  # limit to 2
                pass
            else:
                choosing_pointer += 1
            lcd.mainAdminPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer


def lockerInfo():
    global lockerArray
    current_locker = 1
    showInfo(current_locker)
    # ------------------Button part ------------------
    while True:
        status = button.read()
        if status is "BUT_OK":
            lcd.unlockConfirmPage(current_locker)
            pr.locker_nowBusy(current_locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
            pr.locker(current_locker, pr.OPEN)  # Open locker stand with this user id
            lockerArray[current_locker] = None

            last_millis = datetime.now(timezone.utc)
            while switches.read() is not DOOR[current_locker]:  # if the door is not open
                # then wait
                # wait for 10 seconds, if no signal then automatically use 'No' command
                if (datetime.now(timezone.utc) - last_millis).seconds > PROMPT_WAITING_TIME:
                    break
            # now the door is open!
            time.sleep(2)  # wait for 2 second before proceeding
            pr.locker(current_locker, pr.CLOSE)  # close locker stand with this user id

            # --- wait for the locker is closed
            while switches.read() is not "ALL_CLOSED":  # wait for the locker to be closed
                # wait and print something to debug!
                print(switches.read())
            # --- closed

            return
        elif status is "BUT_CANCEL":
            lcd.clear()
            lcd.mainAdminPage()
            lcd.pointerPos(3, 2)  # choosing_pointer = 2 since the last time
            return  # return to main menu
        elif status is "BUT_UP":
            if current_locker == 20:  # limit to 20 locker
                pass
            else:
                current_locker += 1
            showInfo(current_locker)
        elif status is "BUT_DOWN":
            if current_locker == 1:  # limit to 1
                pass
            else:
                current_locker -= 1
            showInfo(current_locker)


def showInfo(current_locker):
    if lockerArray[current_locker] is None:  # no info
        lcd.clear()
        lcd.infoLockerNoInfoPage(current_locker)
    else:  # info existed
        current_user = lockerArray[current_locker]
        if current_user == TEMPORARY_USER_ID:
            lcd.clear()
            lcd.infoLockerTempPage()
        else:  # a real user
            data = dtb.getInfo(current_user)
            [got_data, user_id, user_name, user_mssv, user_rfid, user_fing] = data
            lcd.clear()
            lcd.infoLockerPage(user_name, user_mssv, current_locker)

    # if current_locker > 20:  # no info found at all
    #     lcd.clear()
    #     lcd.infoLockerNoOnePage()
    #
    #     while button.read() is "BUT_NO_PRESS":
    #         # wait for someone to push any button
    #         pass
    #
    #     lcd.clear()
    #     lcd.mainAdminPage()
    #     lcd.pointerPos(3, choosing_pointer)
    #     return
    # if lockerArray[current_locker] is None:  # no info
    #     pass
    # else:  # info existed
    #     current_user = lockerArray[current_locker]
    #     if current_user == TEMPORARY_USER_ID:
    #         lcd.clear()
    #         lcd.infoLockerTempPage()
    #     else:  # a real user
    #         data = dtb.getInfo(current_user)
    #         [got_data, user_id, user_name, user_mssv, user_rfid, user_fing] = data
    #         lcd.clear()
    #         lcd.infoLockerPage(user_name, user_mssv)


def main():  # Main program block
    # ---------------------------- Setup -------------------------------
    lcd.clear()
    # ---------------------------- Loop -----------------------------------------
    while True:
        lcd.waitPage()

        if rfid.hasID():
            current_tag = rfid.tagID()
            [id_existed, user_id] = dtb.searchRFID(current_tag)
            if id_existed:  # if existed this ID --> User
                userCase(user_id)
            else:  # this ID is not existed in the user database
                if current_tag == ADMIN_KEY:
                    adminCase()
                else:
                    print('RFID not found!')
                    lcd.clear()
                    lcd.unknownIDPage()
                    lcd.pointerPos(3, 1)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        rfid.stop()  # REMEMBER TO DO THIS SINCE THE READING IN C DON'T EXIT BY ITSELF!
        pass
