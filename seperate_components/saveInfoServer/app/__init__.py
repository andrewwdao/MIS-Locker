from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from logging.handlers import RotatingFileHandler
from flask_bootstrap import Bootstrap
import logging
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/error.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.ERROR) # DEBUG, INFO, WARNING, ERROR and CRITICAL
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.ERROR) # DEBUG, INFO, WARNING, ERROR and CRITICAL
    app.logger.info('System startup')

from app import routes, models, errors
