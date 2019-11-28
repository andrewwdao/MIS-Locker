import subprocess
import sys
# Shell = True only when working with c binary file!!!
p = subprocess.Popen(['python3', 'printandwait.py'], shell=False, stdout=subprocess.PIPE)
while True:
    print ("Looping")
    line = p.stdout.readline()
    if not line:
        break
    print(line.strip())
    sys.stdout.flush()
