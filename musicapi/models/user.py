from werkzeug.security import generate_password_hash, check_password_hash

from musicapi.app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password) -> None:
        self.password = generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)
    
    def set_admin(self) -> None:
        self.is_admin = True
    
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return '<User {0} {1}>' .format(self.id, self.username)
    