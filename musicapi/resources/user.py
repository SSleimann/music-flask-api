from sqlalchemy.exc import IntegrityError, NoResultFound

from flask import Blueprint
from flask_restful import Api, Resource
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import create_access_token, jwt_required, current_user

from musicapi.app import db
from musicapi.exceptions import UserNotFoundException
from musicapi.schemas.user import UserSerializationSchema, UserDeserializationSchema
from musicapi.models.user import User

user_bp = Blueprint('user_blueprint', __name__, url_prefix='/user')
api = Api(user_bp)

serializer_schema = UserSerializationSchema()
deserializer_schema = UserDeserializationSchema()

class UserRegisterResource(Resource):
    
    
    def post(self):
        user_register_parser = RequestParser()
        user_register_parser.add_argument('username', type=str, required=True, case_sensitive=True, help='Username is required')
        user_register_parser.add_argument('email', type=str, required=True, help='Email is required')
        user_register_parser.add_argument('password', type=str, required=True, help='Password is required!')
        user_register_parser.add_argument('password_confirmation', type=str, required=True, help='Password confirmation is required')
        args = user_register_parser.parse_args()
        
        data = deserializer_schema.load(args)
        password, _ = data.pop('password', None), data.pop('password_confirmation', None)
 
        user = User(
            **data
        )
        user.set_password(password)
        db.session.add(user)
        
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'This user already exists!'}, 400
        
        return serializer_schema.dump(user), 201
    
class UserLoginResource(Resource):
    
    
    def post(self):
        user_login_parser = RequestParser()
        user_login_parser.add_argument('email', type=str, required=True, help='Email is required')
        user_login_parser.add_argument('password', type=str, required=True, help='Password is required!')
        args = user_login_parser.parse_args()
        
        email, password = args['email'], args['password']
        user = User.query.filter_by(email=email).first()
        
        if not user:
            raise UserNotFoundException
        
        if not user.check_password(password):
            raise UserNotFoundException
        
        token = create_access_token(identity=user)
        
        return {'token': token}, 200        
    
class UserProfileResource(Resource):
    method_decorators = [jwt_required()]
    
    def get(self):
        data = serializer_schema.dump(current_user)
        return data, 200
        
api.add_resource(UserRegisterResource, '/register')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserProfileResource, '/profile')