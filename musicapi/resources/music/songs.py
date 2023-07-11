from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from musicapi.app import db
from musicapi.utils import admin_required
from musicapi.filters import SongFilter
from musicapi.models import Song
from musicapi.exceptions import SongNotFoundException
from musicapi.schemas.music import SongSerializationSchema, SongDeserializationSchema

serialization_schema = SongSerializationSchema()
deserialization_schema = SongDeserializationSchema()

class SongResource(Resource, SongFilter):
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
        
        data = Song.query.paginate(page=page, per_page=10).items
        
        current_app.logger.debug(f'Show songs. pag. {page}, quantity: {len(data)}')
        
        return serialization_schema.dump(data, many=True), 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artists', type=int, action='append', required=True, help='Artist ID is required, can be multiple! [a1, a2]')
        data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
        data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
        data_parser.add_argument('release_date', type=str, required=True, help='Release date is required (YYYY-MM-DD)!')
        args = data_parser.parse_args()
        
        song_data = deserialization_schema.load(args)
        song = Song(**song_data)
        
        db.session.add(song)
        db.session.commit()
        
        current_app.logger.debug(f'Added song: {song}')
        
        data = {
            'message': 'Song created successfully',
            'song': serialization_schema.dump(song)
        }
        
        return data, 201
    
class SongByIdResource(Resource):
    method_decorators = {
        'delete': [admin_required],
        'put': [admin_required]
    }
    
    def get(self, id):
        song = Song.query.get(id)
        
        if song is None:
            raise SongNotFoundException
        
        current_app.logger.debug(f'Show song by id: {song}')
        
        return serialization_schema.dump(song), 200
    
    def delete(self, id):
        song = Song.query.get(id)
        
        if song is None:
            raise SongNotFoundException
        
        db.session.delete(song)
        db.session.commit()
        
        current_app.logger.debug(f'Song with id: {id} has been deleted')
        
        return {'message': 'Song have been deleted successfully'}, 200
    
    def put(self, id):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artists', type=int, action='append', required=True, help='Artist ID is required, can be multiple! [a1, a2]')
        data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
        data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
        data_parser.add_argument('release_date', type=str, required=True, help='Release date is required (YYYY-MM-DD)!')
        args = data_parser.parse_args()
        
        song_data = deserialization_schema.load(args)
        song = Song.query.get(id)
        
        if song is None:
            raise SongNotFoundException
        
        for k, v in song_data.items():
            setattr(song, k, v)
        
        db.session.commit()
        
        data = {
            'message': 'The song was successfully updated!',
            'Artist': serialization_schema.dump(song)
        }
        
        current_app.logger.debug(f'Song with id: {id} has been updated')
        
        return data, 200
    
