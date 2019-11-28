"""------------------------------------------------------------*-
  Main Python file for the saveInfo Server.
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.30 - 19/10/2019
 --------------------------------------------------------------
 *  Server created for the purpose of saving user information
 *
 --------------------------------------------------------------"""
import subprocess
import sys

COMPLIER = 'python3'
TARGET = 'saveInfo.py'

p = subprocess.Popen([COMPLIER, TARGET], shell=False, stdout=subprocess.PIPE)
while True:
    # print ("Looping")
    line = p.stdout.readline()
    if line.strip() == b'save info done':
        print("success!")
        sys.stdout.flush()
        exit()
    sys.stdout.flush()
