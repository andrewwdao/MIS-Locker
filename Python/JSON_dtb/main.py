"""------------------------------------------------------------*-
  JSON database for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Nhat-Khoa Phan 2019
  version 1.00 - 10/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
from JSON_dtb import Database
import time


def main():
    database = Database()

    database.delAllAdmin()
    database.delAllMember()

    database.delAdmin(input('Put your admin RFID here to delete: '))

    database.delMember(input('Put your member MSSV here to delete: '))

    database.addAdmin(input('Put your admin RFID here: '))

    print('First member')
    database.addMember(input('Type in your name: '),
                       input('Type in your MSSV: '),
                       input('Type in your RFID: '),
                       int(input('Type in your FingerPrint number: ')))

    print('Second member')
    database.addMember(input('Type in your name: '),
                       input('Type in your MSSV: '),
                       input('Type in your RFID: '),
                       int(input('Type in your FingerPrint number: ')))

    print('Third member')
    database.addMember(input('Type in your name: '),
                       input('Type in your MSSV: '),
                       input('Type in your RFID: '),
                       int(input('Type in your FingerPrint number: ')))

    fingerTemp = database.searchFinger(int(input('Finger Number you want to search: ')))
    if fingerTemp[0]:
        data = database.getInfo(fingerTemp[1])
        print('Name: '+data[0])
        print('MSSV: '+data[1])

    database.export(True)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
