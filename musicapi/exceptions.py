class ModelNotFoundException(Exception):
    code: int = 404
    message: str = '%s not found!'
    model_name = None
    
    def __init__(self) -> None:
        if self.model_name is None:
            raise ValueError("Model cannot be None")
    
    def response(self) -> dict:
        return {
            "message": self._get_message()
        }, self.code
    
    def _get_message(self) -> str:
        return self.message % self.model_name  
    
    def __str__(self) -> str:
        return self._get_message()
    

class UserNotFoundException(ModelNotFoundException):
    model_name = 'User'

class ArtistNotFoundException(ModelNotFoundException):
    model_name = 'Artist'

class AlbumNotFoundException(ModelNotFoundException):
    model_name = 'Album'
    
class SongNotFoundException(ModelNotFoundException):
    model_name = 'Song'