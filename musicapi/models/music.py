import sqlalchemy as sa

from musicapi.app import db

artist_song_m2m = db.Table('artist_song',
    sa.Column('artist_id', sa.Integer, sa.ForeignKey('artist.id')),
    sa.Column('song_id', sa.Integer, sa.ForeignKey('song.id'))
)

class Artist(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    year_of_birth = sa.Column(sa.DateTime, nullable=False)
    
    albums = db.relationship(
        'Album', 
        backref='artist_albums', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    songs = db.relationship(
        'Song',
        backref='artist_songs',
        lazy='dynamic',
        secondary=artist_song_m2m
    )
    
    def __repr__(self):
        return f'<Artist {self.name}, id {self.id}>'

class Album(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    artist_id = sa.Column(sa.Integer, sa.ForeignKey('artist.id'), nullable=False)
    name = sa.Column(sa.String(20), nullable=False)
    description = sa.Column(sa.Text, nullable=True)
    release_date = sa.Column(sa.DateTime, nullable=False)
    
    songs = db.relationship(
        'Song',
        lazy='dynamic',
        backref='album_songs'
    )
    
    def __repr__(self):
        return f'<Album {self.name}, id {self.id}>'
    
class Song(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(20), nullable=False)
    album_id = sa.Column(sa.Integer, sa.ForeignKey('album.id'), nullable=False)
    duration = sa.Column(sa.Integer, nullable=False)
    release_date = sa.Column(sa.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<Song {self.name}, id {self.id}>'