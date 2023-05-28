from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from musicapi.models import User

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        
    id = auto_field()
    username = auto_field()
    email = auto_field()
    
