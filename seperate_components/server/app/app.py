"""------------------------------------------------------------*-
  Main Python file for the saveInfo Server.
  Tested on: Raspberry Pi 3 B+
  (c) Minh-An Dao 2019
  (c) Miguel Grinberg 2018
  version 1.30 - 19/10/2019
 --------------------------------------------------------------
 *  Server created for the purpose of saving user information
 *
 --------------------------------------------------------------"""
from app import saveInfo_app, db
from app.models import User

@saveInfo_app.shell_context_processor
def make_shell_context():
  return {'db':db,'User':User}
