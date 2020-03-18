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
from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
import logging
import os

saveInfo_app = Flask(__name__)
saveInfo_app.config.from_object(Config)
db = SQLAlchemy(saveInfo_app)
migrate = Migrate(saveInfo_app, db)
bootstrap = Bootstrap(saveInfo_app)
saveInfo_app.config['BOOTSTRAP_SERVE_LOCAL'] = True  # make bootstrap use local resources instead of using online resources

from app.errors import bp as errors_bp
saveInfo_app.register_blueprint(errors_bp)

from app.save_info import bp as save_info_bp
saveInfo_app.register_blueprint(save_info_bp)

if not saveInfo_app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR) # DEBUG, INFO, WARNING, ERROR and CRITICAL
    saveInfo_app.logger.addHandler(file_handler)

    saveInfo_app.logger.setLevel(logging.ERROR) # DEBUG, INFO, WARNING, ERROR and CRITICAL
    saveInfo_app.logger.info('System startup')

from app import models
