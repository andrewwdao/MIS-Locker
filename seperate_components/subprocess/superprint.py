import subprocess
import sys
p = subprocess.Popen(['python', 'printandwait.py'], shell=True, stdout=subprocess.PIPE)
while True:
    print ("Looping")
    line = p.stdout.readline()
    if not line:
        break
    print(line.strip())
    sys.stdout.flush()
