"""*------------------------------------------------------------*-
  Shutdown module in python
    (c) Minh-An Dao 2020
  version 1.00 - 15/03/2020
 --------------------------------------------------------------
 * 
 *
 --------------------------------------------------------------"""
import lcd
import peripheral as pr

lcd.systemClosedPage()
pr.init()    # clear all locks and LEDs before shutdown

