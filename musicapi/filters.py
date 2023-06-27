from flask_restful.reqparse import RequestParser

from musicapi.app import db
from musicapi.models import Artist, Song, Album

class BaseFilter(object):
    model_filter = None
    
    def __init__(self):
        self.parser = RequestParser()
        self.parser.add_argument('search', type=str, help='Search query!', location='args')
        
    def _get_model(self) -> db.Model:
        if self.model_filter is None:
            raise ValueError("Model cannot be None")
        
        if not issubclass(self.model_filter, db.Model):
            raise ValueError("Model filter must be a db.Model")
        
        return self.model_filter
    
    def make_search(self):
        raise NotImplementedError
    
    def make_search_paginated(self):
        raise NotImplementedError
    
    @property
    def parsed_args(self):
        return self.parser.parse_args()
    
class ArtistFilter(BaseFilter):
    model_filter = Artist
    
    def make_search_paginated(self, page: int = 1):
        query = self.parsed_args['search']
        model = self._get_model()
        
        q = model.query.filter(
            model.name.ilike(f'%{query}%')  |
            model.songs.any(Song.name.ilike(f'%{query}%')) | 
            model.albums.any(Album.name.ilike(f'%{query}%')) 
        )
        
        return q.paginate(page=page, per_page=10).items
        
class SongFilter(BaseFilter):
    model_filter = Song
    
    def make_search_paginated(self, page):
        query = self.parsed_args['search']
        model = self._get_model()
        
        q = model.query.filter(
            model.name.ilike(f'%{query}%') |
            model.album_songs.has(Album.name.ilike(f'%{query}%')) |
            model.artist_songs.any(Artist.name.ilike(f'%{query}%'))
        )
        
        return q.paginate(page=page, per_page=10).items

class AlbumFilter(BaseFilter):
    model_filter = Album
    
    def make_search_paginated(self, page):
        query = self.parsed_args['search']
        model = self._get_model()
        
        q = model.query.filter(
            model.name.ilike(f'%{query}%') |
            model.artist_albums.has(Artist.name.ilike(f'%{query}%')) |
            model.songs.any(Song.name.ilike(f'%{query}%'))
        )
        
        return q.paginate(page=page, per_page=10).items