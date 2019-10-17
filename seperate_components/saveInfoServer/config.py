import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Dao_Minh_An_secret_password'
