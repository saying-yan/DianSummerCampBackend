from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserInfo(db.Model):
    __name__ = 'USERINFO'
    uid = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(30))
    phone_number = db.Column(db.String(11))
    password_hash = db.Column(db.String(128))

    def __init__(self, username, phone_number, password_hash):
        self.username = username
        self.phone_number = phone_number
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)