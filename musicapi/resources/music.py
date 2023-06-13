from flask import Blueprint
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date
from flask_jwt_extended import jwt_required, current_user

from musicapi.app import db
from musicapi.models import Artist
from musicapi.schemas.music import ArtistSchema

music_bp = Blueprint('music_blueprint', __name__, url_prefix='/music')
api = Api(music_bp)
schema_artst = ArtistSchema()

class ArtistResource(Resource):     
    def get(self):
        page_parser = RequestParser()
        page_parser.add_argument('page', type=int, location='args')
        args = page_parser.parse_args()
        
        page = 1 if args['page'] is None else args['page']
        data = Artist.query.paginate(page=page, per_page=10).items
        dump = schema_artst.dump(data, many=True)
        
        return dump
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!') 
        data_parser.add_argument('description', type=str) 
        data_parser.add_argument('year_of_birth', type=date, required=True, help='Year of birth is required and the format must be: YYYY-MM-DD') 

        args = data_parser.parse_args()
        
        name, description, year_of_birth = (
            args['name'],
            'Without description!' if args['description'] is None else args['description'], 
            args['year_of_birth']
        )
        
        artist = Artist(name=name, description=description, year_of_birth=year_of_birth)
        db.session.add(artist)
        db.session.commit()
        
        data = {
            'message': 'Artist have been created successfully!',
            'Artist': schema_artst.dump(artist)
        }
        
        return data
        
api.add_resource(ArtistResource, '/artist')