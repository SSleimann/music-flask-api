from flask import Blueprint
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import jwt_required, current_user

from musicapi.app import db

music_bp = Blueprint('music_blueprint', __name__, url_prefix='/music')
api = Api(music_bp)