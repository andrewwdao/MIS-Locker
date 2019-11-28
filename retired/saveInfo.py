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
from app import saveInfo_app

if __name__ == "__main__":
    # use raspberry pi IP address instead of 0.0.0.0 and local IP address for PC (127.0.0.1 - localhost)
    saveInfo_app.run(host='0.0.0.0', port=7497, debug=True)
