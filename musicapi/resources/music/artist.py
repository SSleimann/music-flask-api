from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from musicapi.app import db
from musicapi.models import Artist
from musicapi.filters import ArtistFilter
from musicapi.utils import admin_required, remove_none_values
from musicapi.exceptions import ArtistNotFoundException
from musicapi.schemas.music import ArtistDeserializationSchema, ArtistSerializationSchema

deserialization_schema = ArtistDeserializationSchema()
serialization_schema = ArtistSerializationSchema()

class ArtistResource(Resource, ArtistFilter):
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
        
        data = Artist.query.paginate(page=page, per_page=10).items
        dump = serialization_schema.dump(data, many=True)
        
        current_app.logger.info(f'Show artists. pag. {page}, quantity: {len(data)}')
        
        return dump, 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!') 
        data_parser.add_argument('description', required=True, help='Description is required!', type=str) 
        data_parser.add_argument('year_of_birth', type=str, required=True, help='Year of birth is required and the format must be: YYYY-MM-DD') 
        args = data_parser.parse_args()
        
        artist_data = deserialization_schema.load(args)
        artist = Artist(**artist_data)
        
        db.session.add(artist)
        db.session.commit()
        
        current_app.logger.info(f'A new artist has been created: {artist}')
        
        data = {
            'message': 'Artist have been created successfully!',
            'artist': serialization_schema.dump(artist)
        }
        
        return data, 201
    
class ArtistByIdResource(Resource):
    method_decorators = {
        'delete': [admin_required],
        'put': [admin_required],
        'patch': [admin_required]
    }
    
    def get(self, id):
        artist = db.session.get(Artist, id)
        
        if artist is None:
            raise ArtistNotFoundException
        
        current_app.logger.info(f'Show artist: {artist}')
        
        return serialization_schema.dump(artist), 200
    
    def delete(self, id):
        artist = db.session.get(Artist, id)
        
        if artist is None:
            raise ArtistNotFoundException
        
        db.session.delete(artist)
        db.session.commit()
        
        current_app.logger.info(f'Artist with id: {id} has been deleted')
        
        return {'message': 'Artist have been deleted successfully'}, 200
    
    def put(self, id):
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required!') 
        parser.add_argument('description', type=str, required=True, help='Description is required!') 
        parser.add_argument('year_of_birth', type=str, required=True, help='Year of birth is required and the format must be: YYYY-MM-DD') 
        args = parser.parse_args()
        
        artist_data = deserialization_schema.load(args)
        artist = db.session.get(Artist, id)
        
        if artist is None:
            raise ArtistNotFoundException
        
        for key, value in artist_data.items():
            setattr(artist, key, value)
        
        db.session.commit()
        
        data = {
            'message': 'The artist was successfully updated!',
            'artist': serialization_schema.dump(artist)
        }
        
        current_app.logger.info(f'Artist with id: {id} has been updated')
        
        return data, 200
    
    def patch(self, id):
        parser = RequestParser()
        parser.add_argument('name', type=str, help='Name is required!') 
        parser.add_argument('description', type=str, help='Description is required!') 
        parser.add_argument('year_of_birth', type=str, help='Year of birth is required and the format must be: YYYY-MM-DD') 
        args = parser.parse_args()
        args = remove_none_values(args)
        
        artist_data = deserialization_schema.load(args, partial=True)
        artist = db.session.get(Artist, id)
        
        if artist is None:
            raise ArtistNotFoundException
        
        for key, value in artist_data.items():
            setattr(artist, key, value)
        
        db.session.commit()
        
        data = {
            'message': 'The artist was successfully updated!',
            'artist': serialization_schema.dump(artist)
        }
        
        current_app.logger.info(f'Artist with id: {id} has been updated')
        
        return data, 200
            