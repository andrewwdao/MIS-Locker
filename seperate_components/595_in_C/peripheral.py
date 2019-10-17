"""------------------------------------------------------------*-
  Peripheral controller for Raspberry Pi
  Manipulate 6 IC 74HC595 using C and Subprocess module
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (C) Yasuhiro Ogino 2019
  version 1.00 - 10/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
import subprocess as subpro
import time

pi_dir = "./peripheral_init"
pm_dir = "./peripheral_main "

ON = True
OFF = False

REG_M1_L = 0b00000000  # last
REG_M1_M = 0b00000000  # mid
REG_M1_F = 0b00000000  # first

REG_M2_L = 0b00000000  # last
REG_M2_M = 0b00000000  # mid
REG_M2_F = 0b00000000  # first

BUZZER_BIT = 0b00000001

LOCK01_BIT = 0b00000010
RLED01_BIT = 0b00000100
LOCK02_BIT = 0b00001000
RLED02_BIT = 0b00010000
LOCK03_BIT = 0b00100000
RLED03_BIT = 0b01000000
LOCK04_BIT = 0b10000000
RLED04_BIT = 0b00000010
LOCK05_BIT = 0b00000100
RLED05_BIT = 0b00001000
LOCK06_BIT = 0b00010000
RLED06_BIT = 0b00100000
LOCK07_BIT = 0b01000000
RLED07_BIT = 0b10000000
LOCK08_BIT = 0b00000010
RLED08_BIT = 0b00000100
LOCK09_BIT = 0b00001000
RLED09_BIT = 0b00010000
LOCK10_BIT = 0b00100000
RLED10_BIT = 0b01000000

LOCK11_BIT = 0b00000010
RLED11_BIT = 0b00000100
LOCK12_BIT = 0b00001000
RLED12_BIT = 0b00010000
LOCK13_BIT = 0b00100000
RLED13_BIT = 0b01000000
LOCK14_BIT = 0b10000000
RLED14_BIT = 0b00000010
LOCK15_BIT = 0b00000100
RLED15_BIT = 0b00001000
LOCK16_BIT = 0b00010000
RLED16_BIT = 0b00100000
LOCK17_BIT = 0b01000000
RLED17_BIT = 0b10000000
LOCK18_BIT = 0b00000010
RLED18_BIT = 0b00000100
LOCK19_BIT = 0b00001000
RLED19_BIT = 0b00010000
LOCK20_BIT = 0b00100000
RLED20_BIT = 0b01000000


def init():
    subpro.Popen([pi_dir], shell=True)
    time.sleep(2)  # peripheral start up time


def send():
    subpro.Popen([pm_dir +
                  str(REG_M1_F) + " " +
                  str(REG_M1_M) + " " +
                  str(REG_M1_L) + " " +
                  str(REG_M2_F) + " " +
                  str(REG_M2_M) + " " +
                  str(REG_M2_L)], shell=True)


# def buzzer(state):
#     global REG_M1_F
#     if state:  # on
#         REG_M1_F |= BUZZER_BIT
#     else:      # off
#         REG_M1_F &= ~BUZZER_BIT
#     send()


def lock01(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= LOCK01_BIT
    else:      # off
        REG_M1_F &= ~LOCK01_BIT
    send()


def lock01_busy(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= RLED01_BIT
    else:      # off
        REG_M1_F &= ~RLED01_BIT
    send()


def lock02(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= LOCK02_BIT
    else:      # off
        REG_M1_F &= ~LOCK02_BIT
    send()


def lock02_busy(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= RLED02_BIT
    else:      # off
        REG_M1_F &= ~RLED02_BIT
    send()


def lock03(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= LOCK03_BIT
    else:      # off
        REG_M1_F &= ~LOCK03_BIT
    send()


def lock03_busy(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= RLED03_BIT
    else:      # off
        REG_M1_F &= ~RLED03_BIT
    send()


def lock04(state):
    global REG_M1_F
    if state:  # on
        REG_M1_F |= LOCK04_BIT
    else:      # off
        REG_M1_F &= ~LOCK04_BIT
    send()


def lock04_busy(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= RLED04_BIT
    else:      # off
        REG_M1_M &= ~RLED04_BIT
    send()


def lock05(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= LOCK05_BIT
    else:      # off
        REG_M1_M &= ~LOCK05_BIT
    send()


def lock05_busy(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= RLED05_BIT
    else:      # off
        REG_M1_M &= ~RLED05_BIT
    send()


def lock06(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= LOCK06_BIT
    else:      # off
        REG_M1_M &= ~LOCK06_BIT
    send()


def lock06_busy(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= RLED06_BIT
    else:      # off
        REG_M1_M &= ~RLED06_BIT
    send()


def lock07(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= LOCK07_BIT
    else:      # off
        REG_M1_M &= ~LOCK07_BIT
    send()


def lock07busy(state):
    global REG_M1_M
    if state:  # on
        REG_M1_M |= RLED07_BIT
    else:      # off
        REG_M1_M &= ~RLED07_BIT
    send()


def lock08(state):
    global REG_M1_L
    if state:  # on
        REG_M1_L |= LOCK08_BIT
    else:      # off
        REG_M1_L &= ~LOCK08_BIT
    send()


def lock08_busy(state):
    global REG_M1_L
    if state:  # on
        REG_M1_L |= RLED08_BIT
    else:      # off
        REG_M1_L &= ~RLED08_BIT
    send()


def lock09(state):
    global REG_M1_L
    if state:  # on
        REG_M1_L |= LOCK09_BIT
    else:      # off
        REG_M1_L &= ~LOCK09_BIT
    send()


def lock09_busy(state):
    global REG_M1_L
    if state:  # on
        REG_M1_L |= RLED09_BIT
    else:      # off
        REG_M1_L &= ~RLED09_BIT
    send()


def lock10(state):
    global REG_M1_L
    if state:  # on
        REG_M1_L |= LOCK10_BIT
    else:      # off
        REG_M1_L &= ~LOCK10_BIT
    send()


def lock10_busy(state):
    global REG_M1_L
    if state:  # on
        REG_M1_L |= RLED10_BIT
    else:      # off
        REG_M1_L &= ~RLED10_BIT
    send()


def lock11(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= LOCK11_BIT
    else:      # off
        REG_M2_F &= ~LOCK11_BIT
    send()


def lock11_busy(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= RLED11_BIT
    else:      # off
        REG_M2_F &= ~RLED11_BIT
    send()


def lock12(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= LOCK12_BIT
    else:      # off
        REG_M2_F &= ~LOCK12_BIT
    send()


def lock12_busy(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= RLED12_BIT
    else:      # off
        REG_M2_F &= ~RLED12_BIT
    send()


def lock13(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= LOCK13_BIT
    else:      # off
        REG_M2_F &= ~LOCK13_BIT
    send()


def lock13_busy(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= RLED13_BIT
    else:      # off
        REG_M2_F &= ~RLED13_BIT
    send()


def lock14(state):
    global REG_M2_F
    if state:  # on
        REG_M2_F |= LOCK14_BIT
    else:      # off
        REG_M2_F &= ~LOCK14_BIT
    send()


def lock14_busy(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= RLED14_BIT
    else:      # off
        REG_M2_M &= ~RLED14_BIT
    send()


def lock15(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= LOCK15_BIT
    else:      # off
        REG_M2_M &= ~LOCK15_BIT
    send()


def lock15_busy(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= RLED15_BIT
    else:      # off
        REG_M2_M &= ~RLED15_BIT
    send()


def lock16(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= LOCK16_BIT
    else:      # off
        REG_M2_M &= ~LOCK16_BIT
    send()


def lock16_busy(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= RLED16_BIT
    else:      # off
        REG_M2_M &= ~RLED16_BIT
    send()


def lock17(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= LOCK17_BIT
    else:      # off
        REG_M2_M &= ~LOCK17_BIT
    send()


def lock17_busy(state):
    global REG_M2_M
    if state:  # on
        REG_M2_M |= RLED17_BIT
    else:      # off
        REG_M2_M &= ~RLED17_BIT
    send()


def lock18(state):
    global REG_M2_L
    if state:  # on
        REG_M2_L |= LOCK18_BIT
    else:      # off
        REG_M2_L &= ~LOCK18_BIT
    send()


def lock18_busy(state):
    global REG_M2_L
    if state:  # on
        REG_M2_L |= RLED18_BIT
    else:      # off
        REG_M2_L &= ~RLED18_BIT
    send()


def lock19(state):
    global REG_M2_L
    if state:  # on
        REG_M2_L |= LOCK19_BIT
    else:      # off
        REG_M2_L &= ~LOCK19_BIT
    send()


def lock19_busy(state):
    global REG_M2_L
    if state:  # on
        REG_M2_L |= RLED19_BIT
    else:      # off
        REG_M2_L &= ~RLED19_BIT
    send()


def lock20(state):
    global REG_M2_L
    if state:  # on
        REG_M2_L |= LOCK20_BIT
    else:      # off
        REG_M2_L &= ~LOCK20_BIT
    send()


def lock20_busy(state):
    global REG_M2_L
    if state:  # on
        REG_M2_L |= RLED20_BIT
    else:      # off
        REG_M2_L &= ~RLED20_BIT
    send()

