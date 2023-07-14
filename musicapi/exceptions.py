from musicapi.models import User, Artist, Album, Song

class ExceptionBase(Exception):
    code = None
    message = None
    
    def __init__(self):
        if self.code is None:
            raise ValueError("Code cannot be None")
        
        if self.message is None:
            raise ValueError("Message cannot be None")
    
    def response(self) -> dict:
        return {
            "message": self.message
        }, self.code
    
class ModelNotFoundException(ExceptionBase):
    code: int = 404
    message: str = '%s not found!'
    model = None
    
    def __init__(self) -> None:
        if self.model is None:
            raise ValueError("Model cannot be None")
    
    def response(self) -> dict:
        msg, code = super().response()
        msg['message'] = msg['message'] % self.model.__name__
        
        return msg, code
    
class UserNotAdminException(ExceptionBase):
    code = 403
    message = 'User is not admin'

class UserNotFoundException(ModelNotFoundException):
    model = User

class ArtistNotFoundException(ModelNotFoundException):
    model= Artist

class AlbumNotFoundException(ModelNotFoundException):
    model = Album
    
class SongNotFoundException(ModelNotFoundException):
    model = Song
