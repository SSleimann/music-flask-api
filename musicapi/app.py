import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

from musicapi.config import DevelopmentConfig

db = SQLAlchemy()
migrate = Migrate()
api = Api()
ma = Marshmallow()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    #imports
    from musicapi import models
    from musicapi.resources import user_bp, music_bp
    
    #init apps
    init_apps(app, db)
    
    #load bps
    app.register_blueprint(user_bp)
    app.register_blueprint(music_bp)
    
    return app

def init_apps(app, db):
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)