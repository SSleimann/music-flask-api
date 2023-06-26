from flask import Blueprint
from flask_restful import Api

from musicapi.resources.music.artist import ArtistResource, ArtistByIdResource 
from musicapi.resources.music.albums import AlbumResource, AlbumByIdResource
from musicapi.resources.music.songs import SongResource, SongByIdResource

music_bp = Blueprint('music_blueprint', __name__, url_prefix='/music')
api = Api(music_bp)

api.add_resource(ArtistResource, '/artist')
api.add_resource(ArtistByIdResource, '/artist/<int:id>')

api.add_resource(AlbumResource, '/album')
api.add_resource(AlbumByIdResource, '/album/<int:id>')

api.add_resource(SongResource, '/song')
api.add_resource(SongByIdResource, '/song/<int:id>')