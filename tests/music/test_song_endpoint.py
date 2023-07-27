from sqlalchemy import select

from flask.testing import FlaskClient

from musicapi.models import Song
from musicapi.schemas.music import SongSerializationSchema

serialization_song_schema = SongSerializationSchema()


def test_get_songs(app: FlaskClient, session, auth):
    songs = session.scalars(select(Song)).all()
    data = serialization_song_schema.dump(songs, many=True)

    res = app.get("/music/song", headers={"Authorization": "Bearer {}".format(auth)})

    assert data == res.json
    assert res.status_code == 200


def test_find_song_by_name(app: FlaskClient, session, auth):
    song = session.get(Song, 1)
    data = serialization_song_schema.dump(song)

    res = app.get(
        "/music/song",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": song.name},
    )

    assert data in res.json
    assert res.status_code == 200


def test_find_song_by_artist(app: FlaskClient, session, auth):
    song = session.get(Song, 1)
    song_artist = song.artists.first()

    data = serialization_song_schema.dump(song)

    res = app.get(
        "/music/song",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": song_artist.name},
    )

    assert data in res.json
    assert res.status_code == 200


def test_find_song_by_album(app: FlaskClient, session, auth):
    song = session.get(Song, 1)
    song_album = song.album_songs

    data = serialization_song_schema.dump(song)

    res = app.get(
        "/music/song",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": song_album.name},
    )

    assert data in res.json
    assert res.status_code == 200


def test_get_song_by_id(app: FlaskClient, session, auth):
    song = session.get(Song, 2)
    data = serialization_song_schema.dump(song)

    res = app.get("/music/song/2", headers={"Authorization": "Bearer {}".format(auth)})

    assert res.json == data
    assert res.status_code == 200


def test_post_song(app: FlaskClient, session, auth):
    payload = {
        "name": "pepe",
        "album_id": 2,
        "duration": 200,
        "release_date": "2023-2-2",
        "artists": 1
    }

    res = app.post(
        "/music/song",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload
    )

    song = session.scalar(select(Song).where(Song.name == payload["name"]))

    data_json = dict(
        message="Song created successfully",
        song=serialization_song_schema.dump(song),
    )

    assert song
    assert res.status_code == 201
    assert data_json == res.json


def test_put_song(app: FlaskClient, session, auth):
    payload = {
        "name": "pepe",
        "album_id": 2,
        "duration": 200,
        "release_date": "2023-2-2",
        "artists": [1, 2, 3],
    }

    res = app.put(
        "/music/song/1",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )

    song = session.get(Song, 1)

    data_json = dict(
        message="The song was successfully updated!",
        song=serialization_song_schema.dump(song),
    )
    artists_songs_ids = [artist.id for artist in song.artists.all()]
    artists_songs_ids.sort()
    
    assert song.name == payload["name"]
    assert song.album_id == payload["album_id"]
    assert song.duration == payload["duration"]
    assert artists_songs_ids == payload["artists"]
    assert res.status_code == 200
    assert res.json == data_json

