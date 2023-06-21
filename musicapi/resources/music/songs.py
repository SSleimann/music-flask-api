from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date
from flask_jwt_extended import jwt_required

from musicapi.app import db
from musicapi.models import Song, Artist
from musicapi.schemas.music import SongSchema

schema_song = SongSchema()

class SongResource(Resource):
    def get(self):
        page_parser = RequestParser()
        page_parser.add_argument('page', type=int, location='args')
        args = page_parser.parse_args()
        
        page = 1 if args['page'] is None else args['page']
        data = Song.query.paginate(page=page, per_page=10).items
        
        current_app.logger.debug(f'Show songs. pag. {page}, quantity: {len(data)}')
        
        return schema_song.dump(data, many=True), 200
    
    def post(self):
        data_parser = RequestParser()
        data_parser.add_argument('name', type=str, required=True, help='Name is required!')
        data_parser.add_argument('artist_id', type=int, required=True, help='Artist ID is required!')
        data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
        data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
        data_parser.add_argument('release_date', type=date, required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        
        artist_id = args.pop('artist_id')
        artist = Artist.query.filter(Artist.id == artist_id).first()
        
        if artist is None:
            return {'message': 'Artist not found'}, 404
        
        name, album_id, duration, release_date = (
            args['name'],
            args['album_id'],
            args['duration'],
            args['release_date']
        )
        
        song = Song(name=name, album_id=album_id, duration=duration, release_date=release_date)
        artist.songs.append(song)
        
        db.session.add(song)
        db.session.commit()
        
        current_app.logger.debug(f'A new song has been created: {song}')
        
        data = {
            'message': 'Song have been created successfully!',
            'song': schema_song.dump(song)
        }
        
        return data, 201