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
    def number_of_member(self):
        return User.query.count()

    def getMemberInfoByID(self, member_id):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return [False, None, None, None, None, None]
        else:  # if user existed
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getMemberInfoByMSSV(self, member_mssv):
        user = User.query.filter_by(mssv=member_mssv).first()
        if user is None:  # if user doesn't exist
            return [False, None, None, None, None, None]
        else:  # if user existed
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getMemberInfoByRFID(self, rfid_key):
        user = User.query.filter_by(rfid=rfid_key).first()
        if user is None:  # if user doesn't exist
            return [False, None, None, None, None, None]
        else:  # if user existed
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getLastMemberInfo(self):
        user = User.query.order_by(User.timestamp.desc()).first()
        if user is None:  # if user doesn't exist
            return [False, None, None, None, None, None]
        else:  # if user existed
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]

    def getAllUserInfo(self):
        user = User.query.all()
        print(user)
        return

    def changeInfo(self, member_id, name, mssv):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return False
        else:  # if user existed
            subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
            user.name = name
            user.mssv = mssv
            db.session.commit()
            subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
            return True

    def addDumbUser(self): # create a dumb user with the latest timestamp for server to catch
        subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
        newUser = User()
        db.session.add(newUser)
        db.session.commit()
        subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro

    def addRFID(self, rfid):
        user = User.query.filter_by(rfid=rfid).first()
        if user is None:  # if user doesn't exist yet
            subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
            newUser = User(rfid=rfid)
            db.session.add(newUser)
            db.session.commit()
            subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
            newUser = User.query.filter_by(rfid=rfid).first() # get id from the database
            return [True, newUser.id]
        else:  # if user already existed
            return [False, 0]

    def searchRFID(self, rfid):
        user = User.query.filter_by(rfid=rfid).first()
        if user is None:  # if user doesn't exist
            return [False, 0]
        else:  # if user existed
            return [True, user.id]

    def changeRFID(self, member_id, rfid):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return False
        else:  # if user existed
            subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
            user.rfid = rfid
            db.session.commit()
            subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
            return True

    def addFinger(self, member_id, fingerNum):
        return self.changeFinger(member_id,fingerNum)

    def searchFinger(self, fingerNum):
        user = User.query.filter_by(fing=fingerNum).first()
        if user is None:  # if user doesn't exist
            return [False, 0]
        else:  # if user existed
            return [True, user.id]

    def changeFinger(self, member_id, fingerNum):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return False
        else:  # if user existed
            subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
            user.fing = fingerNum
            db.session.commit()
            subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
            return True

    def delMember(self, member_id):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return False
        else:  # if user existed
            subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
            db.session.delete(user)
            db.session.commit()
            subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro
            return True

    def delAllMember(self):
        users = User.query.all()
        subpro.call(['sudo','mount','-o','remount,rw','/'], shell=False) # turn on rw
        for u in users:
            db.session.delete(u)
        db.session.commit()
        subpro.call(['sudo','mount','-o','remount,ro','/'], shell=False) # turn on ro

