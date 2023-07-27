from flask_restful.reqparse import RequestParser

from musicapi.models import Artist, Song, Album
from musicapi.schemas.music import (
    ArtistSerializationSchema,
    AlbumSerializationSchema,
    SongSerializationSchema,
)


class BaseFilter(object):
    model_filter = None
    serializer_filter = None

    def __init__(self):
        if self.model_filter is None:
            raise ValueError("Model cannot be None")

        if self.serializer_filter is None:
            raise ValueError("Serializer cannot be None")

        parser = RequestParser()
        parser.add_argument("search", type=str, help="Search query!", location="args")

        self._parser_args = parser.parse_args()

    def make_query(self):
        raise NotImplementedError

    def paginate(self, q, page, per_page):
        return q.paginate(page=page, per_page=per_page)

    def make_search_paginated(self):
        raise NotImplementedError

    def response(self, page=None):
        serializer = self.serializer_filter()
        query_data = self.make_query()

        if page:
            query_data = self.paginate(query_data, page=page, per_page=10).items

        data = serializer.dump(query_data, many=True)

        return data, 200

    @property
    def search_args(self):
        return self._parser_args["search"]


class ArtistFilter(BaseFilter):
    model_filter = Artist
    serializer_filter = ArtistSerializationSchema

    def make_query(self):
        query = self.search_args
        model = self.model_filter

        q = model.query.filter(
            model.name.ilike(f"%{query}%")
            | model.songs.any(Song.name.ilike(f"%{query}%"))
            | model.albums.any(Album.name.ilike(f"%{query}%"))
        )

        return q


class AlbumFilter(BaseFilter):
    model_filter = Album
    serializer_filter = AlbumSerializationSchema

    def make_query(self):
        query = self.search_args
        model = self.model_filter

        q = model.query.filter(
            model.name.ilike(f"%{query}%")
            | model.artist_albums.has(Artist.name.ilike(f"%{query}%"))
            | model.songs.any(Song.name.ilike(f"%{query}%"))
        )

        return q


class SongFilter(BaseFilter):
    model_filter = Song
    serializer_filter = SongSerializationSchema

    def make_query(self):
        query = self.search_args
        model = self.model_filter

        q = model.query.filter(
            model.name.ilike(f"%{query}%")
            | model.album_songs.has(Album.name.ilike(f"%{query}%"))
            | model.artists.any(Artist.name.ilike(f"%{query}%"))
        )

        return q
