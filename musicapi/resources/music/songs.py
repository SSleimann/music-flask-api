from flask import current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful.inputs import date
from flask_jwt_extended import jwt_required

from musicapi.app import db
from musicapi.models import Song, Artist, Album
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
        data_parser.add_argument('artist_id', type=int, action='append', required=True, help='Artist ID is required, can be multiple! [a1, a2]')
        data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
        data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
        data_parser.add_argument('release_date', type=date, required=True, help='Release date is required!')
        
        args = data_parser.parse_args()
        
        artists =  [Artist.query.filter(Artist.id == artist_id).first() for artist_id  in args.pop('artist_id') ]
        
        if all([bool(artist) for artist in artists]) is False:
            return {'message': 'One of the artists was not found'}, 404
        
        song = Song(**args)
        
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
            return {'message': 'Song not found'}, 404
        
        current_app.logger.debug(f'Show song by id: {song}')
        
        return schema_song.dump(song), 200
    
    # def put(self, id):
    #     data_parser = RequestParser()
    #     data_parser.add_argument('name', type=str, required=True, help='Name is required!')
    #     data_parser.add_argument('artist_id', type=int, required=True, help='Artist ID is required!')
    #     data_parser.add_argument('album_id', type=int, required=True, help='Album ID is required!')
    #     data_parser.add_argument('duration', type=int, required=True, help='Duration is required (in seconds)')
    #     data_parser.add_argument('release_date', type=date, required=True, help='Release date is required!')
    #     args = data_parser.parse_args()
        
    #     newArtist = db.session.get(Artist, args.pop('artist_id'))
    #     album = db.session.get(Album, args['album_id'])
    #     song = db.session.get(Song, id)
        
    #     if song is None:
    #         return {'message': 'Song not found'}, 404
        
    #     if newArtist is None:
    #         return {'message': 'Artist not found'}, 404
        
    #     if album is None:
    #         return {'message': 'Album not found'}, 404
        
        
    #     oldArtist = song.artist_songs
        
    #     return {"a":"a"}