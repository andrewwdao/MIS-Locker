"""
---------------------------------------------------------------
  Main Python file.
  Server created for the purpose of saving user information
  Raspberry Pi B3+
  (c) Minh-An Dao - 2019
  version 1.00 - 22/09/2019
---------------------------------------------------------------
"""
from app import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
  return {'db':db,'User':User}