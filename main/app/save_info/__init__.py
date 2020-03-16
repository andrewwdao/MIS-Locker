"""------------------------------------------------------------*-
  Init module for Flask server
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.00 - 19/10/2019
 --------------------------------------------------------------
 * Make the server a fully functional package
 *
 --------------------------------------------------------------"""
from flask import Blueprint

bp = Blueprint('save_info', __name__)

from app.save_info import forms, routes