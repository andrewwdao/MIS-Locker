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


class Database:
    def __init__(self):
        with open('database.json', 'r') as inputFile:
            self.dtb = json.load(inputFile)
        self.admin = self.dtb['admin']
        self.member = self.dtb['member']
        self.number_of_admin = len(self.admin)
        self.number_of_member = len(self.member)

    def addAdmin(self, rfid):
        self.admin.append({
            'rfid': rfid
        })
        self.number_of_admin += 1
        with open('database.json', 'w') as outputFile:
            json.dump(self.dtb, outputFile)

    def delAdmin(self, rfid):
        for counter in range(0, self.number_of_admin):
            if self.admin[counter]['rfid'] == rfid:
                del self.admin[counter]
                self.number_of_admin -= 1
                with open('database.json', 'w') as outputFile:
                    json.dump(self.dtb, outputFile)
                return

    def delAllAdmin(self):
        if self.number_of_admin:
            del self.admin[0]
            self.number_of_admin -= 1
            self.delAllAdmin()
        with open('database.json', 'w') as outputFile:
            json.dump(self.dtb, outputFile)

    def addMember(self, name, mssv, rfid, fingerNum):
        self.member.append({
            'name': name,
            'mssv': mssv,
            'rfid': rfid,
            'fing': fingerNum
        })
        self.number_of_member += 1
        with open('database.json', 'w') as outputFile:
            json.dump(self.dtb, outputFile)

    def delMember(self, mssv):
        for counter in range(0, self.number_of_member):
            if self.member[counter]['mssv'] == mssv:
                del self.member[counter]
                self.number_of_member -= 1
                with open('database.json', 'w') as outputFile:
                    json.dump(self.dtb, outputFile)
                return

    def delAllMember(self):
        if self.number_of_member:
            del self.member[0]
            self.number_of_member -= 1
            self.delAllMember()
        with open('database.json', 'w') as outputFile:
            json.dump(self.dtb, outputFile)

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
                with open('database.json', 'w') as outputFile:
                    json.dump(self.dtb, outputFile)
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
                with open('database.json', 'w') as outputFile:
                    json.dump(self.dtb, outputFile)
                return True
        return False

    def getInfo(self, memberNum):
        return [self.member[memberNum]['name'], self.member[memberNum]['mssv']]

