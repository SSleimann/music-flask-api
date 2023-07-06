from musicapi.app import ma
from musicapi.models import Album, Artist, Song

from marshmallow import fields
from dataclasses import field
    
class ArtistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist
        load_instance = True
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field()
    description =ma.auto_field()
    year_of_birth = ma.auto_field()
    num_albums = fields.Method('count_albums')
    num_songs = fields.Method('count_songs')
    total_duration = fields.Method('tt_duration_songs')
    
    def count_albums(self, obj):
        return obj.count_albums
    
    def count_songs(self, obj):
        return obj.count_songs
    
    def tt_duration_songs(self, obj):
        return obj.total_duration_songs
    
class AlbumSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Album
        load_instance = True
        ordered = True
        
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    release_date = ma.auto_field()
    num_songs = fields.Method('count_songs')
    total_duration = fields.Method('tt_duration')
    artist_id = fields.Integer(load_only=True)
    artist_albums = fields.Nested(ArtistSchema, only=('id', 'name'), dump_only=True)
    
    def count_songs(self, obj):
        return obj.count_songs
    
    def tt_duration(self, obj):
        return obj.total_duration
    
class SongSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song
        load_instance = True
        ordered = True
        
    id = ma.auto_field()
    name = ma.auto_field()
    duration = ma.auto_field()
    release_date = ma.auto_field()
    album_id = fields.Integer(load_only=True)
    artist_songs = fields.List(fields.Nested(ArtistSchema, only=('id','name')), dump_only=True)
    album_songs = fields.Nested(AlbumSchema,  only=('id', 'name'), dump_only=True)
    
