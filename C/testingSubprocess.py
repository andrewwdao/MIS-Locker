#NOT WORKING YET!!!
import subprocess as subpro
import sys

try:
    retcode = subpro.call("./main_peripheral" + " 0x00 0x00 0xFF 0x00 0x00 0xFF", shell=True)
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=sys.stderr)
    else:
        print("Child returned", retcode, file=sys.stderr)
except OSError as e:
    print("Execution failed:", e, file=sys.stderr)