import os

import datetime
import environs

env = environs.Env()
env.read_env()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(ROOT_DIR, "logs/api.log")
MIGRATION_DIR = os.path.join(ROOT_DIR, 'migrations')

class Config(object):
    
    
    DEBUG = False
    TESTING = False
    SECRET_KEY = env.str('SECRET_KEY', default='secret')
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY', default='secret')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=6)
    JWT_TOKEN_LOCATION = ['headers']

class DevelopmentConfig(Config):
    
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL', default='sqlite:///dev.sqlite')
    
    