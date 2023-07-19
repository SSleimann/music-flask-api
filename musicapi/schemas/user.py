from marshmallow import fields, validates_schema, ValidationError

from musicapi.app import ma
from musicapi.models import User

class UserDeserializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True
        
    username = ma.auto_field()
    email = fields.Email(required=True)
    password = ma.auto_field(load_only=True)
    password_confirmation = fields.String(required=True, load_only=True)
    
    @validates_schema
    def validates_passwd(self, data, **kwargs):
        if data['password'] != data['password_confirmation']:
            raise ValidationError('Passwords do not match!')
    
class UserSerializationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True
        
    id = ma.auto_field()
    username = ma.auto_field()
    email =ma. auto_field()
    