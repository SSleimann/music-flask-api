import os
import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'ultrasecretkey'
    JWT_SECRET_KEY = 'jwtmegasecretkey'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.sqlite'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)