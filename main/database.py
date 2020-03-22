"""------------------------------------------------------------*-
  Database for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019-2020
  (c) Nhat-Khoa Phan 2019
  version 2.00 - 21/03/2020
 --------------------------------------------------------------
 *
 *
 * 
 --------------------------------------------------------------"""
from app import db
from app.models import User
import subprocess as subpro

# ---------------------------- Private Parameters:
# -----Private variable:


class Database:
    
    def __readwrite(self):
        subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
    
    def __readonly(self):
        subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
    
    def number_of_member(self):
        self.__readwrite()
        counter = User.query.count()
        self.__readonly()
        return counter
        
    def getMemberInfoByID(self, member_id):
        self.__readwrite()
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return [False, None, None, None, None, None]
        else:  # if user existed
            self.__readonly()
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getMemberInfoByMSSV(self, member_mssv):
        self.__readwrite()
        user = User.query.filter_by(mssv=member_mssv).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return [False, None, None, None, None, None]
        else:  # if user existed
            self.__readonly()
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getMemberInfoByRFID(self, rfid_key):
        self.__readwrite()
        user = User.query.filter_by(rfid=rfid_key).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return [False, None, None, None, None, None]
        else:  # if user existed
            self.__readonly()
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getLastMemberInfo(self):
        self.__readwrite()
        user = User.query.order_by(User.timestamp.desc()).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return [False, None, None, None, None, None]
        else:  # if user existed
            self.__readonly()
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getAllUserInfo(self):
        self.__readwrite()
        user = User.query.all()
        print(user)
        self.__readonly()
        return

    def changeInfo(self, member_id, name, mssv):
        self.__readwrite()
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return False
        else:  # if user existed
            user.name = name
            user.mssv = mssv
            db.session.commit()
            self.__readonly()
            return True

    def addDumbUser(self): # create a dumb user with the latest timestamp for server to catch
        self.__readwrite()
        newUser = User()
        db.session.add(newUser)
        db.session.commit()
        self.__readonly()

    def addRFID(self, rfid):
        self.__readwrite()
        user = User.query.filter_by(rfid=rfid).first()
        if user is None:  # if user doesn't exist yet
            newUser = User(rfid=rfid)
            db.session.add(newUser)
            db.session.commit()
            newUser = User.query.filter_by(rfid=rfid).first() # get id from the database
            self.__readonly()
            return [True, newUser.id]
        else:  # if user already existed
            self.__readonly()
            return [False, 0]

    def searchRFID(self, rfid):
        self.__readwrite()
        user = User.query.filter_by(rfid=rfid).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return [False, 0]
        else:  # if user existed
            self.__readonly()
            return [True, user.id]

    def changeRFID(self, member_id, rfid):
        self.__readwrite()
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return False
        else:  # if user existed
            user.rfid = rfid
            db.session.commit()
            self.__readonly()
            return True

    def addFinger(self, member_id, fingerNum):
        return self.changeFinger(member_id,fingerNum)

    def searchFinger(self, fingerNum):
        self.__readwrite()
        user = User.query.filter_by(fing=fingerNum).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return [False, 0]
        else:  # if user existed
            self.__readonly()
            return [True, user.id]

    def changeFinger(self, member_id, fingerNum):
        self.__readwrite()
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return False
        else:  # if user existed
            user.fing = fingerNum
            db.session.commit()
            self.__readonly()
            return True

    def delMember(self, member_id):
        self.__readwrite()
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            self.__readonly()
            return False
        else:  # if user existed
            db.session.delete(user)
            db.session.commit()
            self.__readonly()
            return True

    def delAllMember(self):
        self.__readwrite()
        users = User.query.all()
        for u in users:
            db.session.delete(u)
        db.session.commit()
        self.__readonly()

