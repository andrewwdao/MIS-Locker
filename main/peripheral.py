"""------------------------------------------------------------*-
  Peripheral controller for Raspberry Pi
  Manipulate 6 IC 74HC595 using C and Subprocess module
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019 - 2020
  (C) Yasuhiro Ogino 2019
  version 1.30 - 18/03/2020
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import subprocess as subpro
import time


OPEN = True
CLOSE = False

ON = True
OFF = False

################# For reverse logic ######################

REG_M1_L = 0b11111111  # last
REG_M1_M = 0b11111111  # mid
REG_M1_F = 0b11111111  # first

REG_M2_L = 0b11111111  # last
REG_M2_M = 0b11111111  # mid
REG_M2_F = 0b11111111  # first

################# For forward logic ######################

# REG_M1_L = 0b00000000  # last
# REG_M1_M = 0b00000000  # mid
# REG_M1_F = 0b00000000  # first

# REG_M2_L = 0b00000000  # last
# REG_M2_M = 0b00000000  # mid
# REG_M2_F = 0b00000000  # first

##########################################################

LOCK_BIT = (
    0,
    0b00000010,  # LOCK01_BIT
    0b00001000,  # LOCK02_BIT
    0b00100000,  # LOCK03_BIT
    0b10000000,  # LOCK04_BIT
    0b00000100,  # LOCK05_BIT
    0b00010000,  # LOCK06_BIT
    0b01000000,  # LOCK07_BIT
    0b00000010,  # LOCK08_BIT
    0b00001000,  # LOCK09_BIT
    0b00100000,  # LOCK10_BIT
    0b00000010,  # LOCK11_BIT
    0b00001000,  # LOCK12_BIT
    0b00100000,  # LOCK13_BIT
    0b10000000,  # LOCK14_BIT
    0b00000100,  # LOCK15_BIT
    0b00010000,  # LOCK16_BIT
    0b01000000,  # LOCK17_BIT
    0b00000010,  # LOCK18_BIT
    0b00001000,  # LOCK19_BIT
    0b00100000,  # LOCK20_BIT

    0b00000100,  # RLED01_BIT
    0b00010000,  # RLED02_BIT
    0b01000000,  # RLED03_BIT
    0b00000010,  # RLED04_BIT
    0b00001000,  # RLED05_BIT
    0b00100000,  # RLED06_BIT
    0b10000000,  # RLED07_BIT
    0b00000100,  # RLED08_BIT
    0b00010000,  # RLED09_BIT
    0b01000000,  # RLED10_BIT

    0b00000100,  # RLED11_BIT
    0b00010000,  # RLED12_BIT
    0b01000000,  # RLED13_BIT
    0b00000010,  # RLED14_BIT
    0b00001000,  # RLED15_BIT
    0b00100000,  # RLED16_BIT
    0b10000000,  # RLED17_BIT
    0b00000100,  # RLED18_BIT
    0b00010000,  # RLED19_BIT
    0b01000000,  # RLED20_BIT
)


def init():
    subpro.Popen(['./peripheral_init'], shell=False)


def send():
    subpro.Popen(['./peripheral_main',
                  str(REG_M1_F),
                  str(REG_M1_M),
                  str(REG_M1_L),
                  str(REG_M2_F),
                  str(REG_M2_M),
                  str(REG_M2_L)], shell=False)


################# For reverse logic ######################

def locker(locker_num, state):
    global REG_M1_F, REG_M1_M, REG_M1_L, REG_M2_F, REG_M2_M, REG_M2_L
    if locker_num <= 4:
        if state:  # on
            REG_M1_F &= ~LOCK_BIT[locker_num]  # LOCK0x_BIT
        else:  # off
            REG_M1_F |= LOCK_BIT[locker_num]  # LOCK0x_BIT
    elif locker_num <= 7:
        if state:  # on
            REG_M1_M &= ~LOCK_BIT[locker_num]  # LOCK0x_BIT
        else:  # off
            REG_M1_M |= LOCK_BIT[locker_num]  # LOCK0x_BIT
    elif locker_num <= 10:
        if state:  # on
            REG_M1_L &= ~LOCK_BIT[locker_num]  # LOCK0x_BIT
        else:  # off
            REG_M1_L |= LOCK_BIT[locker_num]  # LOCK0x_BIT
    elif locker_num <= 14:
        if state:  # on
            REG_M2_F &= ~LOCK_BIT[locker_num]  # LOCK1x_BIT
        else:  # off
            REG_M2_F |= LOCK_BIT[locker_num]  # LOCK1x_BIT
    elif locker_num <= 17:
        if state:  # on
            REG_M2_M &= ~LOCK_BIT[locker_num]  # LOCK1x_BIT
        else:  # off
            REG_M2_M |= LOCK_BIT[locker_num]  # LOCK1x_BIT
    elif locker_num <= 20:
        if state:  # on
            REG_M2_L &= ~LOCK_BIT[locker_num]  # LOCK1x_BIT
        else:  # off
            REG_M2_L |= LOCK_BIT[locker_num]  # LOCK1x_BIT
    send()


def locker_nowBusy(locker_num, state):
    global REG_M1_F, REG_M1_M, REG_M1_L, REG_M2_F, REG_M2_M, REG_M2_L
    if locker_num <= 3:
        if state:  # on
            REG_M1_F &= ~LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
        else:  # off
            REG_M1_F |= LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
    elif locker_num <= 7:
        if state:  # on
            REG_M1_M &= ~LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
        else:  # off
            REG_M1_M |= LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
    elif locker_num <= 10:
        if state:  # on
            REG_M1_L &= ~LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
        else:  # off
            REG_M1_L |= LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
    if locker_num <= 13:
        if state:  # on
            REG_M2_F &= ~LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
        else:  # off
            REG_M2_F |= LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
    elif locker_num <= 17:
        if state:  # on
            REG_M2_M &= ~LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
        else:  # off
            REG_M2_M |= LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
    elif locker_num <= 20:
        if state:  # on
            REG_M2_L &= ~LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
        else:  # off
            REG_M2_L |= LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
    send()

################# For forward logic ######################

# def locker(locker_num, state):
#     global REG_M1_F, REG_M1_M, REG_M1_L, REG_M2_F, REG_M2_M, REG_M2_L
#     if locker_num <= 4:
#         if not state:  # on
#             REG_M1_F &= ~LOCK_BIT[locker_num]  # LOCK0x_BIT
#         else:  # off
#             REG_M1_F |= LOCK_BIT[locker_num]  # LOCK0x_BIT
#     elif locker_num <= 7:
#         if not state:  # on
#             REG_M1_M &= ~LOCK_BIT[locker_num]  # LOCK0x_BIT
#         else:  # off
#             REG_M1_M |= LOCK_BIT[locker_num]  # LOCK0x_BIT
#     elif locker_num <= 10:
#         if not state:  # on
#             REG_M1_L &= ~LOCK_BIT[locker_num]  # LOCK0x_BIT
#         else:  # off
#             REG_M1_L |= LOCK_BIT[locker_num]  # LOCK0x_BIT
#     elif locker_num <= 14:
#         if not state:  # on
#             REG_M2_F &= ~LOCK_BIT[locker_num]  # LOCK1x_BIT
#         else:  # off
#             REG_M2_F |= LOCK_BIT[locker_num]  # LOCK1x_BIT
#     elif locker_num <= 17:
#         if not state:  # on
#             REG_M2_M &= ~LOCK_BIT[locker_num]  # LOCK1x_BIT
#         else:  # off
#             REG_M2_M |= LOCK_BIT[locker_num]  # LOCK1x_BIT
#     elif locker_num <= 20:
#         if not state:  # on
#             REG_M2_L &= ~LOCK_BIT[locker_num]  # LOCK1x_BIT
#         else:  # off
#             REG_M2_L |= LOCK_BIT[locker_num]  # LOCK1x_BIT
#     send()


# def locker_nowBusy(locker_num, state):
#     global REG_M1_F, REG_M1_M, REG_M1_L, REG_M2_F, REG_M2_M, REG_M2_L
#     if locker_num <= 3:
#         if not state:  # on
#             REG_M1_F &= ~LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
#         else:  # off
#             REG_M1_F |= LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
#     elif locker_num <= 7:
#         if not state:  # on
#             REG_M1_M &= ~LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
#         else:  # off
#             REG_M1_M |= LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
#     elif locker_num <= 10:
#         if not state:  # on
#             REG_M1_L &= ~LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
#         else:  # off
#             REG_M1_L |= LOCK_BIT[locker_num + 20]  # LOCK0x_BIT
#     if locker_num <= 13:
#         if not state:  # on
#             REG_M2_F &= ~LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
#         else:  # off
#             REG_M2_F |= LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
#     elif locker_num <= 17:
#         if not state:  # on
#             REG_M2_M &= ~LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
#         else:  # off
#             REG_M2_M |= LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
#     elif locker_num <= 20:
#         if not state:  # on
#             REG_M2_L &= ~LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
#         else:  # off
#             REG_M2_L |= LOCK_BIT[locker_num + 20]  # LOCK1x_BIT
#     send()
