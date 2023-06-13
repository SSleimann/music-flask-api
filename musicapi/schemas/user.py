from musicapi.app import ma

from musicapi.models import User

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        
    id = ma.auto_field()
    username = ma.auto_field()
    email =ma. auto_field()
    
