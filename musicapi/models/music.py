import sqlalchemy as sa
from sqlalchemy.event import listens_for
from sqlalchemy.orm import attributes
from sqlalchemy.sql.expression import func, select
from sqlalchemy.ext.hybrid import hybrid_property

from musicapi.app import db

artist_song_m2m = db.Table('artist_song',
    sa.Column('artist_id', sa.Integer, sa.ForeignKey('artist.id'), primary_key=True),
    sa.Column('song_id', sa.Integer, sa.ForeignKey('song.id'), primary_key=True)
)

class Artist(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    year_of_birth = sa.Column(sa.Date, nullable=False)
    
    albums = db.relationship(
        'Album', 
        backref='artist_albums', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    songs = db.relationship(
        'Song',
        back_populates="artists",
        lazy='dynamic',
        secondary=artist_song_m2m
    )
    
    @hybrid_property
    def count_albums(self):
        return self.albums.count()
    
    @hybrid_property
    def count_songs(self):
        return self.songs.count()
    
    @hybrid_property
    def total_duration_songs(self):
        return db.session.query(func.sum(Album.total_duration)).filter(Album.artist_id == self.id).scalar()
    
    def __repr__(self):
        return f'<Artist {self.name}, id {self.id}>'

class Album(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    artist_id = sa.Column(sa.Integer, sa.ForeignKey('artist.id'), nullable=False)
    name = sa.Column(sa.String(20), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    release_date = sa.Column(sa.Date, nullable=False)
    
    songs = db.relationship(
        'Song',
        lazy='dynamic',
        backref='album_songs'
    )
    
    @hybrid_property
    def count_songs(self):
        return self.songs.count()
    
    @hybrid_property
    def total_duration(self):
        return db.session.query(func.sum(Song.duration)).filter(Song.album_id == self.id).scalar()
    
    @total_duration.expression
    def total_duration(self):
        q = (
            select(func.sum(Song.duration))
            .where(Song.album_id == self.id)
            .scalar_subquery()
        )
        
        return q
    
    def __repr__(self):
        return f'<Album {self.name}, id {self.id}>'
    
class Song(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(20), nullable=False)
    album_id = sa.Column(sa.Integer, sa.ForeignKey('album.id'), nullable=True)
    duration = sa.Column(sa.Integer, nullable=False)
    release_date = sa.Column(sa.Date, nullable=False)
    
    artists = db.relationship(
        'Artist',
        lazy='dynamic',
        secondary=artist_song_m2m,
        back_populates="songs"
    )
    
    def __repr__(self):
        return f'<Song {self.name}, id {self.id}>'
    
ctx = {}

@listens_for(Artist, 'after_delete', raw=True)
def artist_after_delete(mapper, connection, target):
    session_id = target.session_id
    ctx[(session_id, 'orphan')] = True

@listens_for(Artist, 'after_update', raw=True)
def artist_after_update(mapper, coneccion, target):
    if target.attrs.songs.history.deleted:
        ctx[(target.session_id, 'orphan')] = True
    
@listens_for(db.session, 'after_flush')
def orphaned_artist_song(session, context):
    if ctx.get((session.hash_key, 'orphan')):
        session.query(Song).filter( ~(Song.artists.any()) ).delete(synchronize_session=False)
        del ctx[(session.hash_key, 'orphan')]