from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date

from musicapi.app import db
from musicapi.utils import admin_required
from musicapi.filters import AlbumFilter
from musicapi.models import Artist, Album
from musicapi.exceptions import AlbumNotFoundException, ArtistNotFoundException
from musicapi.schemas.music import AlbumSchema

schema_album = AlbumSchema()

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
            dump = schema_album.dump(data, many=True)
            return dump, 200 
        
        data = Album.query.paginate(page=page, per_page=10).items
        
        current_app.logger.debug(f'Show albums. pag. {page}, quantity: {len(data)}')
        
        return schema_album.dump(data, many=True), 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, required=True, help='Artist ID is required!')
        data_parser.add_argument('description', type=str, required=True, help='Description is required')
        data_parser.add_argument('release_date', type=lambda x: str(date(x)), required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        
        if Artist.query.filter(Artist.id == args['artist_id']).first() is None:
            raise ArtistNotFoundException
        
        album = schema_album.load(args)
        
        db.session.add(album)
        db.session.commit()
        
        current_app.logger.debug(f'A new album has been created: {album}')
        
        data = {
            'message': 'Album have been created successfully!',
            'album': schema_album.dump(album)
        }
        
        return data, 201
    
class AlbumByIdResource(Resource):
    method_decorators = {
        'delete': [admin_required],
        'put': [admin_required],
        'patch': [admin_required]
    }
    
    def get(self, id):
        album = db.session.get(Album, id)
        
        if album is None:
            raise AlbumNotFoundException
        
        current_app.logger.debug(f'Show album: {album}')
    
        return schema_album.dump(album), 200
    
    def delete(self, id):
        album = db.session.get(Album, id)
        
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
        data_parser.add_argument('release_date', type=date, required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        
        album = db.session.get(Album, id)
        
        if album is None:
            raise AlbumNotFoundException
        
        if Artist.query.filter(Artist.id == args['artist_id']).first() is None:
            raise ArtistNotFoundException
        
        for key, value in args.items():
            setattr(album, key, value)
            
        db.session.commit()
        
        data = {
            'message': 'The album was successfully updated!',
            'Artist': schema_album.dump(album)
        }
        
        current_app.logger.debug(f'Album with id: {id} has been updated')
        return data, 200
    
    def patch(self, id):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, help='Artist ID is required!')
        data_parser.add_argument('description', type=str, help='Description is required')
        data_parser.add_argument('release_date', type=date, help='Release date is required!')
        
        args = data_parser.parse_args()
        
        album = db.session.get(Album, id)
        
        if album is None:
            raise AlbumNotFoundException
        
        if args['artist_id'] is not None and Artist.query.filter(Artist.id == args['artist_id']).first() is None:
            raise ArtistNotFoundException
        
        for key, value in args.items():
            if value is not None:
                setattr(album, key, value)
            
        db.session.commit()
        
        data = {
            'message': 'The album was successfully updated!',
            'Artist': schema_album.dump(album)
        }
        
        current_app.logger.debug(f'Album with id: {id} has been updated')
        return data, 200
                