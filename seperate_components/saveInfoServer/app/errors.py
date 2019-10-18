"""------------------------------------------------------------*-
  Error handler module for Raspberry Pi
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.00 - 18/10/2019
 --------------------------------------------------------------
 *
 *
 --------------------------------------------------------------"""
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500