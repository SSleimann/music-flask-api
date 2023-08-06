import os

import datetime
import environs

env = environs.Env()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(ROOT_DIR, "logs/api.log")
MIGRATION_DIR = os.path.join(ROOT_DIR, 'migrations')

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = env.str('SECRET_KEY', default='secret')
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY', default='secret')
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=6)
    JWT_TOKEN_LOCATION = ['headers']
    LOG_LEVEL = env.log_level("LOG_LEVEL", default='DEBUG')
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT=120
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL', default='sqlite:///dev.sqlite')
    LOG_LEVEL = env.log_level("LOG_LEVEL", default='INFO')
    CACHE_TYPE = 'RedisCache'
    
class TestingConfig(Config):
    TESTING = True
    LOG_LEVEL = env.log_level("LOG_LEVEL", default='DEBUG')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_db.sqlite'
    