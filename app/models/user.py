from jwt import encode, decode
from flask import g
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
from config import SECRET_KEY

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    avatar_url = db.Column(db.String(256))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("Password is not readable attribute.")

    @password.setter
    def password(self, new_password):
        self.password_hash = generate_password_hash(new_password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def safe_avatar_url(self):
        return self.avatar_url or "https://media.discordapp.net/attachments/600712545757822976/929305078765088818/390046883281633290.png"

    def generate_auth_token(self):
        payload = {
            "uid": self.id,
            "phs": self.password_hash
        }
        return encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_auth_token(token):
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        return User.query.filter_by(id=payload.get("uid"),
                                    password_hash=payload.get("phs")).first()
