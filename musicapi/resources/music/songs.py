from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date

from musicapi.app import db
from musicapi.filters import SongFilter
from musicapi.models import Song, Artist, Album
from musicapi.exceptions import ArtistNotFoundException, AlbumNotFoundException, SongNotFoundException
from musicapi.schemas.music import SongSchema

schema_song = SongSchema()


class SongResource(Resource, SongFilter):

    
    def get(self):
        page_parser = RequestParser()
        page_parser.add_argument('page', type=int, location='args')
        args = page_parser.parse_args()
        
        page = 1 if args['page'] is None else args['page']
        
        if self.parsed_args['search'] is not None:
            data = self.make_search_paginated(page=page)
            dump = schema_song.dump(data, many=True)
            return dump, 200 
        
        data = Song.query.paginate(page=page, per_page=10).items
        
        current_app.logger.debug(f'Show songs. pag. {page}, quantity: {len(data)}')
        
        return schema_song.dump(data, many=True), 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, action='append', required=True, help='Artist ID is required, can be multiple! [a1, a2]')
        data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
        data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
        data_parser.add_argument('release_date', type=lambda x: str(date(x)), required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        artists_id = args.pop('artist_id')
        
        if Album.query.filter(Album.id == args['album_id']).first() is None:
            raise AlbumNotFoundException
        
        artists =  Artist.query.filter(Artist.id.in_(artists_id)).all()
        
        if not artist:
            raise ArtistNotFoundException
        
        song = schema_song.load(args)
        
        for artist in artists:
            artist.songs.append(song)
        
        db.session.add(song)
        db.session.commit()
        
        current_app.logger.debug(f'Added song: {song}')
        
        data = {
            'message': 'Song created successfully',
            'song': schema_song.dump(song)
        }
        
        return data, 201
    
class SongByIdResource(Resource):
    
    def get(self, id):
        song = db.session.get(Song, id)
        
        if song is None:
            raise SongNotFoundException
        
        current_app.logger.debug(f'Show song by id: {song}')
        
        return schema_song.dump(song), 200
    
    def delete(self, id):
        song = db.session.get(Song, id)
        
        if song is None:
            raise SongNotFoundException
        
        db.session.delete(song)
        db.session.commit()
        
        current_app.logger.debug(f'Song with id: {id} has been deleted')
        
        return {'message': 'Song have been deleted successfully'}, 200
    
    def put(self, id):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, action='append', required=True, help='Artist ID is required, can be multiple! [a1, a2]')
        data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
        data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
        data_parser.add_argument('release_date', type=date, required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        song = db.session.get(Song, id)
        artists_id = args.pop('artist_id')
        
        if song is None:
            raise SongNotFoundException
        
        if Album.query.filter(Album.id == args['album_id']).first() is None:
            raise AlbumNotFoundException
        
        artists_args = Artist.query.filter(Artist.id.in_(artists_id)).all()
        
        if not artists_args:
            raise ArtistNotFoundException
        
        song.artist_songs = artists_args
        
        for k, v in args.items():
            setattr(song, k, v)
        
        db.session.commit()
        
        data = {
            'message': 'The song was successfully updated!',
            'Artist': schema_song.dump(song)
        }
        
        current_app.logger.debug(f'Song with id: {id} has been updated')
        
        return data, 200
    
