import lcd
from adc import adc_button, adc_switches
from rfid import RDM6300
from database import Database
import peripheral as pr
from datetime import datetime, timezone
# import fingerPrint
from app import saveInfo_app
import time

# ---------------------------- Configurable parameters -------------------------
# -----Admin ID key:
ADMIN_KEY = '810093B8D6\r\n'
PROMPT_WAITING_TIME = 8
# TEMPORARY_USER_ID = 9999
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
# fingerPrint.begin()
# fingerPrint.activate()

# next_locker_available = 1  # next available locker (default at 1)
# database id stand with locker that has been rented (20 locker)
# omit index 0!!!
# lockerArray = ["NULL", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
#                None, None, None, None, None]
lockerArray = ["NULL", None, None, None]
NO_ID = 999999

def dumpDebug(iid, name, mssv, rrfid, fing):
    print('member_id: ' + str(iid))
    print('Name: ' + str(name))
    print('MSSV: ' + str(mssv))
    print('RFID: ' + str(rrfid))
    print('fingerNumber: ' + str(fing))


def openDoorProcedure(locker):
    pr.locker_nowBusy(locker, pr.OFF)  # CLOSE RED LED stand with this LOCKER
    pr.locker(locker, pr.OPEN)  # Open locker stand with this user id

    last_millis = datetime.now(timezone.utc)
    while switches.read() is not DOOR[locker]:  # if the door is not open
        # then wait
        # wait for 10 seconds, if no signal then automatically use 'No' command
        if (datetime.now(timezone.utc) - last_millis).seconds > PROMPT_WAITING_TIME:
            break
        # if human push ok button
        if button.read() is "BUT_OK":
            pr.locker(locker, pr.CLOSE)  # close locker stand with this user id
            return
    # now the door is open!
    time.sleep(2)  # wait for 2 second before proceeding
    pr.locker(locker, pr.CLOSE)  # close locker stand with this user id

    # --- wait for the locker is closed
    while switches.read() is not "ALL_CLOSED":  # wait for the locker to be closed
        # wait and print something to debug!
        print(switches.read())
        # if human push ok button
        if button.read() is "BUT_OK":
            pr.locker(locker, pr.CLOSE)  # close locker stand with this user id
            return
    # --- closed
    return


def getNextAvailableLocker():
    if None in lockerArray:  # if still have vacancy
        next_locker_available = lockerArray.index(None)
        return next_locker_available
    else:  # no vacancy left
        return None


def waitForConfirmation():
    time.sleep(0.4)  # prevent debounce
    while button.read() is not "BUT_OK":
        # wait for someone to push any button
        pass


def userCase(userID):
    global lockerArray
    data = dtb.getMemberInfoByID(userID)
    [got_data, user_id, user_name, user_mssv, user_rfid, user_fing] = data

    if got_data:  # if get info from database successfully
        # ------------  OLD LOCKER!!! -----------------
        if user_id in lockerArray:  # if user is renting a locker
            current_locker = lockerArray.index(user_id)
            lcd.clear()
            lcd.returnPage(user_name, current_locker)  # Name, locker_num
            lockerArray[current_locker] = user_id
            openDoorProcedure(current_locker)

            pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

            dumpDebug(user_id, user_name, user_mssv, user_rfid, user_fing)

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
            # global next_locker_available
            # current_locker = next_locker_available
            # if None in lockerArray:  # if still have vacancy
            #     next_locker_available = lockerArray.index(None)  # automatically set to the lowest locker available
            current_locker = getNextAvailableLocker()
            if current_locker is None:  # out of vacancy
                lcd.clear()
                lcd.outOfVacancy()

                waitForConfirmation()

                lcd.clear()
                return
            else:  # new locker available
                lcd.clear()
                lcd.welcomePage(user_name, user_mssv, current_locker)  # Name, mssv, locker_num
                lockerArray[current_locker] = user_id
                openDoorProcedure(current_locker)

                pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

                dumpDebug(user_id, user_name, user_mssv, user_rfid, user_fing)

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

                waitForConfirmation()

                lcd.clear()
                lcd.mainAdminPage()
                lcd.pointerPos(3, choosing_pointer)

            elif choosing_pointer == 2:  # Locker info command
                lockerInfo()
                lcd.clear()
                lcd.mainAdminPage()
                lcd.pointerPos(3, 2)  # choosing_pointer = 2 since the last time

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
    time.sleep(1)  # stabilize time
    # ------------------Button part ------------------
    while True:
        status = button.read()
        if status is "BUT_OK":
            lcd.clear()
            lcd.unlockConfirmPage(current_locker)
            lockerArray[current_locker] = None
            openDoorProcedure(current_locker)
            return
        elif status is "BUT_CANCEL":
            lcd.clear()
            lcd.mainAdminPage()
            lcd.pointerPos(3, 2)  # choosing_pointer = 2 since the last time
            return  # return to main menu
        elif status is "BUT_UP":
            if current_locker == (len(lockerArray)-1):  # limit to 20 locker
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
    lcd.clear()
    if lockerArray[current_locker] is None:  # no info
        lcd.clear()
        lcd.infoLockerNoInfoPage(current_locker)
    else:  # info existed
        current_user = lockerArray[current_locker]
        if current_user is not int:
            lcd.clear()
            lcd.infoLockerTempPage(current_locker)
        else:  # a real user
            data = dtb.getInfo(current_user)
            user_name = data[2]
            user_mssv = data[3]
            lcd.clear()
            lcd.infoLockerPage(user_name, user_mssv, current_locker)


def oneTimeUserCase(current_tag):
    current_locker = getNextAvailableLocker()
    if current_locker is None:  # out of vacancy
        lcd.clear()
        lcd.outOfVacancyPage()

        waitForConfirmation()

        lcd.clear()
        return
    else:  # new locker available
        lcd.clear()
        lcd.welcomeTempPage(current_locker)
        lockerArray[current_locker] = current_tag
        openDoorProcedure(current_locker)

        pr.locker_nowBusy(current_locker, pr.ON)  # OPEN RED LED stand with this LOCKER

        lcd.clear()
        return


def oneTimeUser_returnCase(current_tag):
    current_locker = lockerArray.index(current_tag)  # get the locker out
    lcd.clear()
    lcd.returnTempPage(current_locker)
    openDoorProcedure(current_locker)
    lockerArray[current_locker] = None

    lcd.clear()
    return


def addNewIDCase():
    user_id = NO_ID  # create user id
    # add RFID
    [status_rfid, user_id_rfid] = addRFID()
    # now time to add fingerPrint
    [status_fing, user_id_fing] = addFingerPrint(status_rfid, user_id)

    if status_rfid or status_fing:  # rfid or fing is available
        if user_id_rfid != user_id_fing:
            if user_id_fing == NO_ID:
                user_id = user_id_rfid
            elif user_id_rfid == NO_ID:
                user_id = user_id_fing
        else:  # they are equal
            user_id = user_id_rfid

        if user_id == NO_ID:
            raise Exception("Error with database, please check again")

        # Add personal information
        lcd.clear()
        lcd.addNewInfo()
        saveInfo_app.run(host='0.0.0.0', port=7497, debug=False)  # run collecting app

        data = dtb.getLastMemberInfo()
        user_valid = data[0]
        user_id = data[1]
        user_name = data[2]
        user_mssv = data[3]
        if user_valid:
            if (user_name and user_mssv) is not None:
                userCase(user_id)
                return
            return
        return
    else:  # no rfid or fingerPrint is available
        choosing_pointer = 2  # because we are at the Add new ID
        lcd.clear()
        lcd.unknownIDPage()
        lcd.pointerPos(3, choosing_pointer)
        return  # return to No Info menu


def addRFID():
    lcd.clear()
    lcd.addRFIDPage()
    rfid.flush()  # clear everything before starting
    while True:
        lcd.addRFIDPage()
        # wait for signal here
        if rfid.hasID():
            current_tag = rfid.tagID()
            [status, user_id] = dtb.addRFID(current_tag)
            if status:  # RFID added
                lcd.clear()
                lcd.addRFIDSuccessPage()
                waitForConfirmation()
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
                            lcd.addRFIDPage()
                            rfid.flush()  # clear everything before starting
                            break
                        elif choosing_pointer == 2: # cancel
                            return [False, NO_ID]
                        return [False, NO_ID]
                    elif status is "BUT_CANCEL":
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

        if button.read() is "BUT_CANCEL":
            return [False, NO_ID]


def addFingerPrint(status_rfid, user_id):
    lcd.clear()
    lcd.addFingerPage()
    while True:
        # fingerPrint.first_enroll()
        # ...
        if button.read() is "BUT_CANCEL":
            return [False, NO_ID]


def addExistedIDCase():
    lcd.clear()
    lcd.addExtraInfoPage()
    while True:
        lcd.addExtraInfoPage()
        if rfid.hasID():
            current_tag = rfid.tagID()
            [id_existed, user_id] = dtb.searchRFID(current_tag)
            if id_existed:  # if existed this ID --> User
                lcd.clear()
                data = dtb.getMemberInfoByID(user_id)
                user_name = data[2]
                user_mssv = data[3]
                lcd.addExtraMainPage(user_name, user_mssv)
                choosing_pointer = 2  # default at first position
                lcd.pointerPos(3, choosing_pointer)
                # ------------------Button part ------------------
                while True:
                    status = button.read()
                    if status is "BUT_OK":
                        if choosing_pointer == 2:  # Add/Change RFID
                            ChangeRFID(user_id)
                            return
                        elif choosing_pointer == 3:  # Add/Change Finger
                            ChangeFinger(user_id)
                            return
                    elif status is "BUT_CANCEL":
                        return
                    elif status is "BUT_UP":
                        if choosing_pointer == 2:  # limit to 2
                            pass
                        else:
                            choosing_pointer -= 1
                        lcd.addExtraMainPage(user_name, user_mssv)
                        lcd.pointerPos(3, choosing_pointer)
                    elif status is "BUT_DOWN":
                        if choosing_pointer == 3:  # limit to 2
                            pass
                        else:
                            choosing_pointer += 1
                        lcd.addExtraMainPage(user_name, user_mssv)
                        lcd.pointerPos(3, choosing_pointer)
            else:  # this ID is not existed in the user database
                if current_tag in lockerArray:  # temporary user
                    oneTimeUser_returnCase(current_tag)


def ChangeRFID(user_id):
    lcd.clear()
    lcd.addRFIDPage()
    rfid.flush()  # clear everything before starting
    while True:
        lcd.addRFIDPage()
        # wait for signal here
        if rfid.hasID():
            current_tag = rfid.tagID()
            if dtb.changeRFID(user_id, current_tag):  # if RFID changed successfully
                lcd.clear()
                lcd.addRFIDSuccessPage()
                waitForConfirmation()
                return True
            else:
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
                            lcd.addRFIDPage()
                            rfid.flush()  # clear everything before starting
                            break
                        elif choosing_pointer == 2:  # cancel
                            return False
                        return False
                    elif status is "BUT_CANCEL":
                        return False
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
            return False


def ChangeFinger(user_id):
    lcd.clear()
    lcd.addFingerPage()
    while True:
        # fingerPrint.first_enroll()
        # ...
        if button.read() is "BUT_CANCEL":
            return False


def noInfoCase(current_tag):
    choosing_pointer = 1  # default at first position
    lcd.clear()
    lcd.unknownIDPage()
    lcd.pointerPos(3, choosing_pointer)
    while True:
        status = button.read()
        if status is "BUT_OK":
            if choosing_pointer == 1:  # One-time user command
                oneTimeUserCase(current_tag)
                lcd.clear()
                return
            elif choosing_pointer == 2:  # Add new ID command
                addNewIDCase()
                lcd.clear()
                return

            elif choosing_pointer == 3:  # Add existed ID command
                addExistedIDCase()
                lcd.clear()
                return

        elif status is "BUT_CANCEL":
            lcd.clear()
            return  # return to waiting state
        elif status is "BUT_UP":
            if choosing_pointer == 1:  # limit to 1
                pass
            else:
                choosing_pointer -= 1
            lcd.unknownIDPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer
        elif status is "BUT_DOWN":
            if choosing_pointer == 3:  # limit to 3
                pass
            else:
                choosing_pointer += 1
            lcd.unknownIDPage()
            lcd.pointerPos(3, choosing_pointer)  # option, pointer


def main():  # Main program block
    # ---------------------------- Setup -------------------------------
    lcd.clear()
    print("System ready!")
    # ---------------------------- Loop -----------------------------------------
    while True:
        lcd.waitPage()

        if rfid.hasID():
            current_tag = rfid.tagID()
            [id_existed, user_id] = dtb.searchRFID(current_tag)
            if id_existed:  # if existed this ID --> User
                userCase(user_id)
            else:  # this ID is not existed in the user database
                if current_tag in lockerArray:  # temporary user
                    oneTimeUser_returnCase(current_tag)
                elif current_tag == ADMIN_KEY:
                    adminCase()
                else:
                    print('RFID not found!')
                    noInfoCase(current_tag)
            rfid.flush()  # flush out old buffer before get out


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        lcd.clear()
        rfid.stop()  # REMEMBER TO DO THIS SINCE THE READING IN C DON'T EXIT BY ITSELF!
        pass
