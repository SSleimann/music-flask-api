from werkzeug.security import generate_password_hash, check_password_hash

from musicapi.app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def set_paswword(self, password) -> None:
        self.password = generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)
    
