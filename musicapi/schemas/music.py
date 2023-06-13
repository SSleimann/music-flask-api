from musicapi.app import ma

from musicapi.models import Album, Artist, Song
    
class SongSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song
        load_instance = True
        
    name = ma.auto_field()
    album_id = ma.auto_field()
    duration = ma.auto_field()
    release_date = ma.auto_field()
    
class AlbumSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Album
        load_instance = True
        
    artist_id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    release_date = ma.auto_field()
    songs = ma.Nested(SongSchema, many=True)
    
class ArtistSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist
        load_instance = True
    
    name = ma.auto_field()
    description =ma.auto_field()
    year_of_birth = ma.auto_field()
    
    songs = ma.Nested(SongSchema, many=True)
    albums = ma.Nested(AlbumSchema, many=True)