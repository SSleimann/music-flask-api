from sqlalchemy import select

from flask.testing import FlaskClient

from musicapi.models import Song
from musicapi.schemas.music import SongSerializationSchema

serialization_song_schema = SongSerializationSchema()

def test_get_songs(app: FlaskClient, session, auth):
    songs = session.scalars(select(Song)).all()
    data = serialization_song_schema.dump(songs, many=True)
    
    res = app.get(
        '/music/song',
        headers={"Authorization": "Bearer {}".format(auth)}
    )
    
    assert data == res.json
    assert res.status_code == 200
    
def test_find_song_by_name(app: FlaskClient, session, auth):
    song = session.get(Song, 1)
    data = serialization_song_schema.dump(song)
    
    res = app.get(
        '/music/song',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': song.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_find_song_by_artist(app: FlaskClient, session, auth):
    song = session.get(Song, 1)
    song_artist = song.artists.first()
    
    data = serialization_song_schema.dump(song)
    
    res = app.get(
        '/music/song',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': song_artist.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_find_song_by_album(app: FlaskClient, session, auth):
    song = session.get(Song, 1)
    song_album = song.album_songs
    
    data = serialization_song_schema.dump(song)
    
    res = app.get(
        '/music/song',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': song_album.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_get_song_by_id(app: FlaskClient, session, auth):
    song = session.get(Song, 2)
    data = serialization_song_schema.dump(song)
    
    res = app.get(
        '/music/song/{}'.format(2),
        headers={"Authorization": "Bearer {}".format(auth)}
    )
    
    assert res.json == data
    assert res.status_code == 200