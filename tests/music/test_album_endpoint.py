from sqlalchemy import select

from flask.testing import FlaskClient

from musicapi.models import Album
from musicapi.schemas.music import AlbumSerializationSchema

serialization_album_schema = AlbumSerializationSchema()


def test_get_albums(app: FlaskClient, session, auth):
    albums = session.scalars(select(Album)).all()
    data = serialization_album_schema.dump(albums, many=True)

    res = app.get("/music/album", headers={"Authorization": "Bearer {}".format(auth)})

    assert res.json == data
    assert res.status_code == 200


def test_find_album_by_name(app: FlaskClient, session, auth):
    album = session.get(Album, 1)
    data = serialization_album_schema.dump(album)

    res = app.get(
        "/music/album",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": album.name},
    )

    assert data in res.json
    assert res.status_code == 200


def test_find_album_by_artist(app: FlaskClient, session, auth):
    album = session.get(Album, 1)
    album_artist = album.artist_albums

    data = serialization_album_schema.dump(album)

    res = app.get(
        "/music/album",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": album_artist.name},
    )

    assert data in res.json
    assert res.status_code == 200


def test_find_album_by_song(app: FlaskClient, session, auth):
    album = session.get(Album, 1)
    album_song = album.songs.first()

    data = serialization_album_schema.dump(album)

    res = app.get(
        "/music/album",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": album_song.name},
    )

    assert data in res.json
    assert res.status_code == 200


def test_get_album_by_id(app: FlaskClient, session, auth):
    album = session.get(Album, 2)
    data = serialization_album_schema.dump(album)

    res = app.get("/music/album/2", headers={"Authorization": "Bearer {}".format(auth)})

    assert res.json == data
    assert res.status_code == 200


def test_post_album(app: FlaskClient, session, auth):
    payload = {
        "artist_id": 1,
        "name": "albumpandita",
        "description": "hello album",
        "release_date": "2021-3-16",
    }

    res = app.post(
        "/music/album",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )

    album = session.scalar(select(Album).where(Album.name == payload["name"]))

    data_json = dict(
        message="Album have been created successfully!",
        album=serialization_album_schema.dump(album),
    )
    
    assert album
    assert res.status_code == 201
    assert data_json == res.json

def test_put_album(app: FlaskClient, session, auth):
    payload = {
        "artist_id": 3,
        "name": "albumormal",
        "description": "bye album",
        "release_date": "2021-3-17",
    }
    
    res = app.put(
        "/music/album/3",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )
    
    album = session.get(Album, 3)
    
    data_json = dict(
        message='The album was successfully updated!',
        album=serialization_album_schema.dump(album)
    )
    
    assert album.name == payload['name']
    assert album.description == payload['description']
    assert album.artist_id == payload['artist_id']
    assert res.status_code == 200
    assert res.json == data_json

def test_patch_album(app: FlaskClient, session, auth):
    payload = {
        "artist_id": 1,
    }
    
    res = app.patch(
        "/music/album/3",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )
    
    album = session.get(Album, 3)
    
    data_json = dict(
        message='The album was successfully updated!',
        album=serialization_album_schema.dump(album)
    )
    
    assert album.artist_id == payload['artist_id']
    assert res.status_code == 200
    assert res.json == data_json