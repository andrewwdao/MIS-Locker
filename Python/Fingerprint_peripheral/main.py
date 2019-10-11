import fingerPrint

PI_DIR = "./peripheral_init"
 = "./peripheral_main " + "0" + " " + "0" + " " + "0" + " " + "0" + " " + "0" + " " + "0"
pm2_dir = "./peripheral_main " + "12" + " " + "34" + " " + "56" + " " + "12" + " " + "34" + " " + "56"

fingerPrint.begin()
fingerPrint.activate()
try:
    while True:
        fingerPrint.check()
    #  print(fingerPrint.enroll())

    # print(fingerPrint.check())

    # print(fingerPrint.delete(5))
except KeyboardInterrupt:
    pass
