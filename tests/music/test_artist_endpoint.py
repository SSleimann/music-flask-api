from sqlalchemy import select, inspect

from flask.testing import FlaskClient

from musicapi.models import Artist
from musicapi.schemas.music import ArtistSerializationSchema

serialization_artist_schema = ArtistSerializationSchema()


def test_get_artists(app: FlaskClient, session, auth):
    artists = session.scalars(select(Artist)).all()
    data = serialization_artist_schema.dump(artists, many=True)

    res = app.get("/music/artist", headers={"Authorization": "Bearer {}".format(auth)})

    assert res.json == data
    assert res.status_code == 200


def test_find_artist_by_name(app: FlaskClient, session, auth):
    artist = session.get(Artist, 1)
    data = serialization_artist_schema.dump(artist)

    res = app.get(
        "/music/artist",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": artist.name},
    )

    assert res.json[0] == data
    assert res.status_code == 200


def test_find_artist_by_album(app: FlaskClient, session, auth):
    artist = session.get(Artist, 1)
    artist_album = artist.albums.first()

    data = serialization_artist_schema.dump(artist)

    res = app.get(
        "/music/artist",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": artist_album.name},
    )

    assert res.json[0] == data
    assert res.status_code == 200


def test_find_artist_by_song(app: FlaskClient, session, auth):
    artist = session.get(Artist, 1)
    artist_song = artist.songs.first()

    data = serialization_artist_schema.dump(artist)

    res = app.get(
        "/music/artist",
        headers={"Authorization": "Bearer {}".format(auth)},
        query_string={"search": artist_song.name},
    )

    assert res.json[0] == data
    assert res.status_code == 200


def test_get_artist_by_id(app: FlaskClient, session, auth):
    artist = session.get(Artist, 2)
    data = serialization_artist_schema.dump(artist)

    res = app.get(
        "/music/artist/2",
        headers={"Authorization": "Bearer {}".format(auth)},
    )

    assert res.json == data
    assert res.status_code == 200


def test_post_artist(app: FlaskClient, session, auth):
    payload = {
        "name": "juan",
        "description": "hello firends",
        "year_of_birth": "2023-1-12",
    }

    res = app.post(
        "/music/artist",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )

    artist = session.scalar(select(Artist).where(Artist.name == payload["name"]))
    
    data_json = dict(
        message="Artist have been created successfully!",
        artist=serialization_artist_schema.dump(artist),
    )
    
    assert res.status_code == 201
    assert res.json == data_json
    assert artist


def test_put_artist(app: FlaskClient, session, auth):
    payload = {
        "name": "juan",
        "description": "hello firends",
        "year_of_birth": "2023-1-12",
    }

    res = app.put(
        "/music/artist/1",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )

    artist = session.get(Artist, 1)

    data_json = dict(
        message="The artist was successfully updated!",
        artist=serialization_artist_schema.dump(artist),
    )

    assert res.status_code == 200
    assert res.json == data_json
    assert artist.name == payload["name"]
    assert artist.description == payload["description"]


def test_patch_artist(app: FlaskClient, session, auth):
    payload = {
        "name": "juan23",
    }

    res = app.patch(
        "/music/artist/4",
        headers={"Authorization": "Bearer {}".format(auth)},
        json=payload,
    )

    artist = session.get(Artist, 4)

    data_json = dict(
        message="The artist was successfully updated!",
        artist=serialization_artist_schema.dump(artist),
    )
    
    assert res.status_code == 200
    assert res.json == data_json
    assert artist.name == payload["name"]
