"""*------------------------------------------------------------*-
    Startup module for MISlocker in python
    (c) Minh-An Dao 2020
    version 1.00 - 17/03/2020
 --------------------------------------------------------------
 * 
 *
 --------------------------------------------------------------"""
import subprocess as subpro
import lcd

subpro.Popen(['./peripheral_init'], shell=False) # set peripherals to low
lcd.begin()# dipslay LCD at startup

