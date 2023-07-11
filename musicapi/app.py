import os

import logging

from flask import Flask
from flask.logging import default_handler
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

from marshmallow import ValidationError

from musicapi.exceptions import ExceptionBase
from musicapi.config import DevelopmentConfig, LOG_DIR, MIGRATION_DIR

db = SQLAlchemy()
migrate = Migrate()
api = Api()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ensure the instance folder exists and the log folder
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    try:
        os.makedirs(LOG_DIR)
    except OSError:
        pass
    
    #imports
    from musicapi import models
    
    #init apps
    init_apps(app, db)
    
    #load bps
    load_blueprints(app)
    
    #load error handlers
    load_error_handlers(app)
    
    #configure logger
    config_logger(app)
    
    return app

def init_apps(app, db):
    db.init_app(app)
    migrate.init_app(app, db, directory=MIGRATION_DIR)
    api.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    
def load_blueprints(app):
    from musicapi.resources import user_bp
    from musicapi.resources.music import music_bp
    
    app.register_blueprint(user_bp)
    app.register_blueprint(music_bp)
    
def config_logger(app):
    app.logger.removeHandler(default_handler)
    
    formatter = logging.Formatter(
        "[%(asctime)s] - %(levelname)s in %(module)s - [%(name)s.%(funcName)s:%(lineno)d] - %(message)s"
    )
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(LOG_DIR, 'a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.DEBUG)

def load_error_handlers(app):
    
    @app.errorhandler(ExceptionBase)
    def handle_model_not_found(e):
        return e.response()
    
    @app.errorhandler(ValidationError)
    def marshmallow_validation_error(e):
        return  {'errors': e.messages}, 422