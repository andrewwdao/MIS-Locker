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
from database import Database


def main():
    database = Database()

    # database.delMember(int(input('Put your member id here to delete: ')))
    # database.delAllMember()

    # print('First member')
    # database.addFinger(input("Put your Finger number here: "))
    fingerTemp = database.searchFinger(int(input('Finger Number you want to search: ')))
    if fingerTemp[0]:
        data = database.getInfo(fingerTemp[1])
        if data[0]:
            print('member_id: ' + str(data[1]))
            print('Name: '+str(data[2]))
            print('MSSV: '+str(data[3]))
            print('RFID: '+str(data[4]))
            print('fingerNumber: '+str(data[5]))
        else:
            print('some error occurred')
    else:
        print('Fingerprint not found!')


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
