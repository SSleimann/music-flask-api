from sqlalchemy import select

from flask.testing import FlaskClient

from musicapi.models import Artist
from musicapi.schemas.music import ArtistSerializationSchema

serialization_artist_schema = ArtistSerializationSchema()

def test_get_artists(app: FlaskClient, session, auth):
    artists = session.scalars(select(Artist)).all()
    data = serialization_artist_schema.dump(artists, many=True)
    
    res = app.get(
        '/music/artist',
        headers={"Authorization": "Bearer {}".format(auth)}
    )
    
    assert res.json == data
    assert res.status_code == 200
    
def test_find_artist_by_name(app: FlaskClient, session, auth):
    artist = session.get(Artist, 1)
    data = serialization_artist_schema.dump(artist)
    
    res = app.get(
        '/music/artist',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': artist.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_find_artist_by_album(app: FlaskClient, session, auth):
    artist = session.get(Artist, 1)
    artist_album = artist.albums.first()
    
    data = serialization_artist_schema.dump(artist)
    
    res = app.get(
        '/music/artist',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': artist_album.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_find_artist_by_song(app: FlaskClient, session, auth):
    artist = session.get(Artist, 1)
    artist_song = artist.songs.first()
    
    data = serialization_artist_schema.dump(artist)
    
    res = app.get(
        '/music/artist',
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={'search': artist_song.name}
    )
    
    assert res.json[0] == data
    assert res.status_code == 200

def test_get_artist_by_id(app: FlaskClient, session, auth):
    artist = session.get(Artist, 2)
    data = serialization_artist_schema.dump(artist)
    
    res = app.get(
        '/music/artist/{}'.format(2),
        headers={"Authorization": "Bearer {}".format(auth)}
    )
    
    assert res.json == data
    assert res.status_code == 200