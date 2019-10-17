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
import json
from cryptography.fernet import Fernet
# ---------------------------- Private Parameters:
# -----Private key and CBC:
AUTH_KEY = 'AadQrY8DTxdEAVjvgXObPZtZiVtQrpU3HYDlFJUO0Vg='
DATABASE_FILE = 'dtb'
EXPORTED_FILE = 'database.json'


class Database:
    def __init__(self):
        with open(DATABASE_FILE, 'rb') as inputFile:
            self.enc_dtb = inputFile.read()
        self.crypter = Fernet(AUTH_KEY)
        dec_string = self.crypter.decrypt(self.enc_dtb).decode()
        self.dec_dtb = json.loads(dec_string)
        self.admin = self.dec_dtb['admin']
        self.member = self.dec_dtb['member']
        self.number_of_admin = len(self.admin)
        self.number_of_member = len(self.member)

    def update(self):
        self.enc_dtb = self.crypter.encrypt((json.dumps(self.dec_dtb)).encode())
        with open(DATABASE_FILE, 'wb') as outputFile:
            outputFile.write(self.enc_dtb)

    def export(self, beautiful):
        if beautiful:
            with open(EXPORTED_FILE, 'w') as outputFile:
                json.dump(self.dec_dtb, outputFile, indent=4)
        else:
            with open(EXPORTED_FILE, 'w') as outputFile:
                json.dump(self.dec_dtb, outputFile)

    def addAdmin(self, rfid):
        self.admin.append({
            'rfid': rfid
        })
        self.number_of_admin += 1
        self.update()

    def delAdmin(self, rfid):
        for counter in range(0, self.number_of_admin):
            if self.admin[counter]['rfid'] == rfid:
                del self.admin[counter]
                self.number_of_admin -= 1
                self.update()
                return

    def delAllAdmin(self):
        if self.number_of_admin:
            del self.admin[0]
            self.number_of_admin -= 1
            self.delAllAdmin()
        self.update()

    def addMember(self, name, mssv, rfid, fingerNum):
        self.member.append({
            'name': name,
            'mssv': mssv,
            'rfid': rfid,
            'fing': fingerNum
        })
        self.number_of_member += 1
        self.update()

    def delMember(self, mssv):
        for counter in range(0, self.number_of_member):
            if self.member[counter]['mssv'] == mssv:
                del self.member[counter]
                self.number_of_member -= 1
                self.update()
                return

    def delAllMember(self):
        if self.number_of_member:
            del self.member[0]
            self.number_of_member -= 1
            self.delAllMember()
        self.update()

    def searchAdmin(self, rfid):
        for counter in range(0, self.number_of_admin):
            if self.admin[counter]['rfid'] == rfid:
                return [True, counter]
        return [False, 9999]

    def searchRFID(self, rfid):
        for counter in range(0, self.number_of_member):
            if self.member[counter]['rfid'] == rfid:
                return [True, counter]
        return [False, 9999]

    def changeRFID(self, mssv, rfid):
        for counter in range(0, self.number_of_member):
            if self.member[counter]['mssv'] == mssv:
                self.member[counter]['rfid'] = rfid
                self.update()
                return True
        return False

    def searchFinger(self, fingerNum):
        for counter in range(0, self.number_of_member):
            if self.member[counter]['fing'] == fingerNum:
                return [True, counter]
        return [False, 9999]

    def changeFinger(self, mssv, fingerNum):
        for counter in range(0, self.number_of_member):
            if self.member[counter]['mssv'] == mssv:
                self.member[counter]['fing'] = fingerNum
                self.update()
                return True
        return False

    def getInfo(self, memberNum):
        return [self.member[memberNum]['name'], self.member[memberNum]['mssv']]

