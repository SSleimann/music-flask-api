from musicapi.app import db
from musicapi.models.music import Artist, Album, Song
from musicapi.dummy_data import songs, albums, artists
from musicapi.schemas.music import ArtistDeserializationSchema, AlbumDeserializationSchema, SongDeserializationSchema

class DummyHelper:
    def add_dummy_data(self):
        artists_des = ArtistDeserializationSchema().load(artists, many=True)
        artists_obj = [ Artist(**data) for data in artists_des  ]
        
        db.session.add_all(artists_obj)
        db.session.commit()
        
        albums_des = AlbumDeserializationSchema().load(albums, many=True)
        albums_obj = [ Album(**data) for data in albums_des  ]
        
        db.session.add_all(albums_obj)
        db.session.commit()
        
        songs_des = SongDeserializationSchema().load(songs, many=True, session=db.session)
        songs_obj = [ Song(**data) for data in songs_des  ]
        
        db.session.add_all(songs_obj)
        db.session.commit()