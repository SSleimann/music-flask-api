from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date
from flask_jwt_extended import jwt_required

from musicapi.app import db
from musicapi.models import Artist, Album
from musicapi.schemas.music import AlbumSchema

schema_album = AlbumSchema()

class AlbumResource(Resource):
    
    
    def get(self):
        page_parser = RequestParser()
        page_parser.add_argument('page', type=int, location='args')
        args = page_parser.parse_args()
        
        page = 1 if args['page'] is None else args['page']
        data = Album.query.paginate(page=page, per_page=10).items
        
        current_app.logger.debug(f'Show albums. pag. {page}, quantity: {len(data)}')
        
        return schema_album.dump(data, many=True), 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, required=True, help='Artist ID is required!')
        data_parser.add_argument('description', type=str, required=True, help='Description is required')
        data_parser.add_argument('release_date', type=date, required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        name, artist_id, description, release_date = (
            args['name'], 
            args['artist_id'], 
            args['description'], 
            args['release_date']
        )
        
        album = Album(name=name, artist_id=artist_id, description=description, release_date=release_date)
        
        db.session.add(album)
        db.session.commit()
        
        current_app.logger.debug(f'A new album has been created: {album}')
        
        data = {
            'message': 'Album have been created successfully!',
            'album': schema_album.dump(album)
        }
        
        return data, 201