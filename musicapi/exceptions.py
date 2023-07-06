class ExceptionBase(Exception):
    code = None
    message = None
    
    def _get_code(self) -> int:
        if self.code is None:
            raise ValueError("Code cannot be None")
        
        return self.code
    
    def _get_message(self):
        if self.message is None:
            raise ValueError("Message cannot be None")
        
        return self.message
    
    def response(self) -> dict:
        return {
            "message": self._get_message()
        }, self._get_code()
    
class ModelNotFoundException(ExceptionBase):
    code: int = 404
    message: str = '%s not found!'
    model_name = None
    
    def __init__(self) -> None:
        if self.model_name is None:
            raise ValueError("Model cannot be None")
    
    def _get_message(self) -> str:
        msg = super()._get_message()
        
        return msg % self.model_name  
    
    def __str__(self) -> str:
        return self._get_message()
    
class UserNotAdminException(ExceptionBase):
    code = 403
    message = 'User is not admin'

class UserNotFoundException(ModelNotFoundException):
    model_name = 'User'

class ArtistNotFoundException(ModelNotFoundException):
    model_name = 'Artist'

class AlbumNotFoundException(ModelNotFoundException):
    model_name = 'Album'
    
class SongNotFoundException(ModelNotFoundException):
    model_name = 'Song'
