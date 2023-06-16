from musicapi.app import ma
from musicapi.models import Album, Artist, Song
    
from marshmallow import fields
class SongSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song
        load_instance = True
        
    id = ma.auto_field()
    name = ma.auto_field()
    album_id = ma.auto_field()
    duration = ma.auto_field()
    release_date = ma.auto_field()
    
class AlbumSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Album
        load_instance = True
        
    id = ma.auto_field()
    artist_id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    release_date = ma.auto_field()
    num_songs = fields.Method('count_songs')
    
    def count_songs(self, obj):
        return obj.count_songs()
    
class ArtistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist
        load_instance = True
    
    id = ma.auto_field()
    name = ma.auto_field()
    description =ma.auto_field()
    year_of_birth = ma.auto_field()
    num_albums = fields.Method('count_albums')
    num_songs = fields.Method('count_songs')
    
    def count_albums(self, obj):
        return obj.count_albums
    
    def count_songs(self, obj):
        return obj.count_songs