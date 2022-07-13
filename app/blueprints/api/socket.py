from app import socketio, db
from app.models.user import User

@socketio.on("connect")
def on_user_connect(auth):
    user = db.get_user(id=User.decode_auth_token(auth.get("token")).get("id"))
    if not auth or not user:
        raise ConnectionError("Incorrect credentials")
    print(f"{user.username} ({user.id}) connected to the party!")
