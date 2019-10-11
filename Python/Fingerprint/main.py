import fingerPrint

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
