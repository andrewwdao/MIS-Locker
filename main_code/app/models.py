"""------------------------------------------------------------*-
  Model module for Flask server
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.00 - 19/10/2019
 --------------------------------------------------------------
 * Defines database columns and tables
 *
 --------------------------------------------------------------"""
from hashlib import md5
from app import db
from datetime import datetime, timezone


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    mssv = db.Column(db.String(8), index=True, unique=True)
    rfid = db.Column(db.String(13), index=True, unique=True)
    fing = db.Column(db.Integer, index=True, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(timezone.utc))

    def __repr__(self):
        return '<User {}>'.format(self.mssv)
