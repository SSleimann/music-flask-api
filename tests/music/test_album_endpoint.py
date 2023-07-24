from sqlalchemy import select

from flask.testing import FlaskClient

from musicapi.models import Album
from musicapi.schemas.music import AlbumSerializationSchema

serialization_album_schema = AlbumSerializationSchema()

def test_get_albums(app: FlaskClient, session, auth):
    albums = session.scalars(select(Album)).all()
    data = serialization_album_schema.dump(albums, many=True)
    
    res = app.get(
        '/music/album',
        headers={"Authorization": "Bearer {}".format(auth)}
    )
    
    assert res.json == data
    assert res.status_code == 200
    
def test_find_album_by_name(app: FlaskClient, session, auth):
    album = session.get(Album, 1)
    data = serialization_album_schema.dump(album)
    
    res = app.get(
        '/music/album',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': album.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_find_album_by_artist(app: FlaskClient, session, auth):
    album = session.get(Album, 1)
    album_artist = album.artist_albums
    
    data = serialization_album_schema.dump(album)
    
    res = app.get(
        '/music/album',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': album_artist.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_find_album_by_song(app: FlaskClient, session, auth):
    album = session.get(Album, 1)
    album_song = album.songs.first()
    
    data = serialization_album_schema.dump(album)
    
    res = app.get(
        '/music/album',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': album_song.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_get_album_by_id(app: FlaskClient, session, auth):
    album = session.get(Album, 2)
    data = serialization_album_schema.dump(album)
    
    res = app.get(
        '/music/album/{}'.format(2),
        headers={"Authorization": "Bearer {}".format(auth)}
    )
    
    assert res.json == data
    assert res.status_code == 200