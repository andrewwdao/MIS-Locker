"""*------------------------------------------------------------*-
  Shutdown server - python module file
  Tested with RASPBERRY PI 3B+
    (c) Minh-An Dao 2020
  version 1.00 - 29/03/2019
 --------------------------------------------------------------
 * 
 *
 --------------------------------------------------------------"""
import os
import time
import sys
import signal

time.sleep(1)
print(sys.argv[1])
os.kill(int(sys.argv[1]),signal.SIGINT) # find out the current task it's running on, then kill it
