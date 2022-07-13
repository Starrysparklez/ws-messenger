from flask import request
from app import db
from app.models.user import User

def decode_user(request) -> User:
    """Decode token and get user data from the database."""
    token = request.headers.get("Authorization")
    if not token:
        raise AttributeError("Provide an authorization token.")
    try:
        data = User.decode_auth_token(token)
        if type(data.get('id')) != str:
            raise TypeError('User ID should be string.')
        if type(data.get('password_hash')) != str:
            raise TypeError('Password hash should be string.')
        user = db.get_user(**data)
    except RuntimeError:
        raise AttributeError("Invalid credentials.")
    if not user:
        raise AttributeError("Invalid credentials.")
    return user
