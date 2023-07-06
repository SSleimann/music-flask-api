from flask_jwt_extended import current_user

from functools import wraps

from musicapi.exceptions import UserNotAdminException

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            raise UserNotAdminException
        return func(*args, **kwargs)
    return wrapper