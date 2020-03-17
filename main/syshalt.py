"""*------------------------------------------------------------*-
  Shutdown module for MISlocker in python
    (c) Minh-An Dao 2020
  version 1.10 - 17/03/2020
 --------------------------------------------------------------
 * 
 *
 --------------------------------------------------------------"""
import subprocess as subpro
import lcd

subpro.Popen(['./peripheral_init'], shell=False) # clear all locks and LEDs before shutdown
lcd.systemClosedPage()
