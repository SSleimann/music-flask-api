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

def remove_none_values(dict: dict) -> dict:
    return { k:v for k, v in dict.items() if v is not None } 