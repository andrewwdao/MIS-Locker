"""------------------------------------------------------------*-
  Database for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Nhat-Khoa Phan 2019
  version 1.00 - 10/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
from app import db
from app.models import User


# ---------------------------- Private Parameters:
# -----Private variable:


class Database:
    def number_of_member(self):
        return User.query.count()

    def addRFID(self, rfid):
        user = User.query.filter_by(rfid=rfid).first()
        if user is None:  # if user doesn't exist yet
            newUser = User(rfid=rfid)
            db.session.add(newUser)
            db.session.commit()
            newUser = User.query.order_by(User.id.desc()).first()  # get the last user out (user we just added)
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
            user.rfid = rfid
            db.session.commit()
            return True

    def addFinger(self, fingerNum):
        user = User.query.filter_by(fing=fingerNum).first()
        if user is None:  # if user doesn't exist yet
            newUser = User(fing=fingerNum)
            db.session.add(newUser)
            db.session.commit()
            newUser = User.query.order_by(User.id.desc()).first()  # get the last user out (user we just added)
            return [True, newUser.id]
        else:  # if user already existed
            return [True, 0]

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
            user.fing = fingerNum
            db.session.commit()
            return True

    def delMember(self, member_id):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return False
        else:  # if user existed
            db.session.delete(user)
            db.session.commit()
            return True

    def delAllMember(self):
        users = User.query.all()
        for u in users:
            db.session.delete(u)
        db.session.commit()

    def getInfo(self, member_id):
        user = User.query.filter_by(id=member_id).first()
        if user is None:  # if user doesn't exist
            return [False, None, None, None, None, None]
        else:  # if user existed
            return [True, user.id, user.name, user.mssv, user.rfid, user.fing]
