from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from musicapi.app import db
from musicapi.utils import admin_required, remove_none_values
from musicapi.filters import AlbumFilter
from musicapi.models import Album
from musicapi.exceptions import AlbumNotFoundException
from musicapi.schemas.music import AlbumSerializationSchema, AlbumDeserializationSchema

deserialization_schema = AlbumDeserializationSchema()
serialization_schema = AlbumSerializationSchema()

class AlbumResource(Resource, AlbumFilter):
    method_decorators = {
        'post': [admin_required]
    }
    
    def get(self):
        page_parser = RequestParser()
        page_parser.add_argument('page', type=int, location='args')
        args = page_parser.parse_args()
        
        page = 1 if args['page'] is None else args['page']
        
        if self.parsed_args['search'] is not None:
            data = self.make_search_paginated(page=page)
            dump = serialization_schema.dump(data, many=True)
            return dump, 200 
        
        data = Album.query.paginate(page=page, per_page=10).items
        
        current_app.logger.debug(f'Show albums. pag. {page}, quantity: {len(data)}')
        
        return serialization_schema.dump(data, many=True), 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, required=True, help='Artist ID is required!')
        data_parser.add_argument('description', type=str, required=True, help='Description is required')
        data_parser.add_argument('release_date', type=str, required=True, help='Release date is required (YYYY-MM-DD)!')
        args = data_parser.parse_args()
        
        album_data = deserialization_schema.load(args)
        album = Album(**album_data)
        
        db.session.add(album)
        db.session.commit()
        
        current_app.logger.debug(f'A new album has been created: {album}')
        
        data = {
            'message': 'Album have been created successfully!',
            'album': serialization_schema.dump(album)
        }
        
        return data, 201
    
class AlbumByIdResource(Resource):
    method_decorators = {
        'delete': [admin_required],
        'put': [admin_required],
        'patch': [admin_required]
    }
    
    def get(self, id):
        album = Album.query.get(id)
        
        if album is None:
            raise AlbumNotFoundException
        
        current_app.logger.debug(f'Show album: {album}')
    
        return serialization_schema.dump(album), 200
    
    def delete(self, id):
        album = Album.query.get(id)
        
        if album is None:
            raise AlbumNotFoundException
        
        db.session.delete(album)
        db.session.commit()
        
        current_app.logger.debug(f'Album with id: {id} has been deleted')
    
        return {'message': 'Album have been deleted successfully'}, 200
        
    def put(self, id):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, required=True, help='Artist ID is required!')
        data_parser.add_argument('description', type=str, required=True, help='Description is required')
        data_parser.add_argument('release_date', type=str, required=True, help='Release date is required (YYYY-MM-DD)!')
        args = data_parser.parse_args()
        
        album_data = deserialization_schema.load(args)
        album = Album.query.get(id)
        
        if album is None:
            raise AlbumNotFoundException
        
        for key, value in album_data.items():
            setattr(album, key, value)
            
        db.session.commit()
        
        data = {
            'message': 'The album was successfully updated!',
            'Album': serialization_schema.dump(album)
        }
        
        current_app.logger.debug(f'Album with id: {id} has been updated')
        return data, 200
    
    def patch(self, id):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, help='Artist ID is required!')
        data_parser.add_argument('description', type=str, help='Description is required')
        data_parser.add_argument('release_date', type=str, help='Release date is required (YYYY-MM-DD)!')
        args = data_parser.parse_args()
        args = remove_none_values(args)
        
        album_data = deserialization_schema.load(args, partial=True)
        album = Album.query.get(id)
        
        if album is None:
            raise AlbumNotFoundException
        
        for key, value in album_data.items():
            setattr(album, key, value)
            
        db.session.commit()
        
        data = {
            'message': 'The album was successfully updated!',
            'Album': serialization_schema.dump(album)
        }
        
        current_app.logger.debug(f'Album with id: {id} has been updated')
        return data, 200
                