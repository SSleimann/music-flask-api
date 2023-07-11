from sqlalchemy.exc import NoResultFound

from musicapi.app import ma
from musicapi.models import Album, Artist, Song

from marshmallow import fields, validate, validates, ValidationError, post_load

class ArtistDeserializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field( validate=validate.Length(min=3, max=20) )
    description = ma.auto_field()
    year_of_birth = ma.auto_field()

class ArtistSerializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Artist
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field()
    description =ma.auto_field()
    year_of_birth = ma.auto_field()
    num_albums = fields.Integer(attribute='count_albums')
    num_songs = fields.Integer(attribute='count_songs')
    total_duration_songs =  fields.Integer()
    
class AlbumDeserializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Album
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field( validate=validate.Length(min=3, max=20) )
    description = ma.auto_field()
    release_date = ma.auto_field()
    artist_id = ma.auto_field()
    
    @validates('artist_id')
    def validate_artist_id(self, value):
        artist = Artist.query.get(value)
        
        if artist is None:
            raise ValidationError('Artist does not exist!')
        
class AlbumSerializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Album
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field()
    release_date = ma.auto_field()
    
    num_songs = fields.Integer(attribute='count_songs')
    total_duration_songs =  fields.Integer(attribute='total_duration')
    artist = fields.Nested(ArtistSerializationSchema(only=('id', 'name')), attribute='artist_albums')
    
class SongDeserializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field( validate=validate.Length(min=3, max=40) )
    duration = ma.auto_field()
    release_date = ma.auto_field()
    album_id = ma.auto_field()
    artists = ma.auto_field()
    
    @validates('album_id')
    def validate_album_id(self, value):
        album = Album.query.get(value)
        
        if album is None:
            raise ValidationError('Album does not exist!')
    
class SongSerializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Song
        ordered = True
    
    id = ma.auto_field()
    name = ma.auto_field()
    duration = ma.auto_field()
    release_date = ma.auto_field()
    album = fields.Nested(AlbumSerializationSchema(only=('id', 'name')), attribute='album_songs')
    artists = fields.Nested(ArtistSerializationSchema(only=('id', 'name')), many=True)
    
