"""*------------------------------------------------------------*-
  Shutdown server - python module file
  Tested with RASPBERRY PI 3B+
    (c) Minh-An Dao 2020
  version 1.00 - 29/03/2019
 --------------------------------------------------------------
 * 
 *
 * ref: https://www.tutorialspoint.com/python/python_command_line_arguments.htm
 * 
 --------------------------------------------------------------"""
import os
import time
import sys
import signal

# ======================= Take the parameter pass in as a pid number and kill it ========================
time.sleep(1)
# print(sys.argv[1]) # for debugging webserver pid - sys.argv[1] = os.getpid()
os.kill(int(sys.argv[1]),signal.SIGINT) # find out the current task it's running on, then kill it
