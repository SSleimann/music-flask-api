from musicapi.app import jwt
from musicapi.models import User

from musicapi.resources.user import user_bp
from musicapi.resources.music import music_bp

#jwt
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()