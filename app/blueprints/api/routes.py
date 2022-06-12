from traceback import print_exc as print_exception
from app.models.text_channel import TextChannel
from app.models.message import Message
from flask import Blueprint, request
from flask_socketio import (
    emit,
    join_room,
    leave_room,
    ConnectionRefusedError as ConnectionError,
)
from app.models.user import User
from app import db, csrf, socketio
from copy import copy

api = Blueprint("api", __name__)


def decode_user(request) -> User:
    token = request.headers.get("Authorization")
    if not token:
        raise AttributeError("Provide an authorization token.")
    try:
        user = db.get_user(**User.decode_auth_token(token))
    except RuntimeError:
        raise AttributeError("Invalid credentials.")
    if not user:
        raise AttributeError("Invalid credentials.")
    return user


# ------


@api.route("/user", methods=("GET",))
@csrf.exempt
def api_user_info():
    try:
        user = decode_user(request)
    except Exception as error:
        return {"error": str(error)}, 400

    return {"user": user.to_json()}


@api.route("/channels", methods=("GET",))
@csrf.exempt
def api_channel_list():
    try:
        user = decode_user(request)
    except Exception as error:
        print_exception()
        return {"error": str(error)}, 400

    channels = db.get_all_text_channels() or []
    return {
        "total_channels": len(channels),
        "channels_data": [x.to_json() for x in channels],
    }, 200


@api.route("/channel", methods=("GET", "PUT", "DELETE", "PATCH"))
@csrf.exempt
def api_channel():
    try:
        user = decode_user(request)
    except Exception as error:
        print_exception()
        return {"error": str(error)}, 400

    data = request.json

    if request.method == "GET":
        channel = db.get_text_channel(id=int(data.get("id")))
        if channel:
            return channel.to_json(), 200
        return {"error": "NOT FOUND"}, 404

    if request.method == "PUT":
        try:
            channel = TextChannel(
                name=data.get("name"), description=data.get("description")
            )
            db.create_text_channel(channel)
        except Exception:
            print_exception()
            return {"error": "ERR"}, 500
        socketio.emit("channel_create", channel.to_json(), broadcast=True)
        return {"message": "OK"}, 200

    if request.method == "DELETE":
        try:
            channel = db.get_text_channel(id=int(data.get("id")))
            if not channel:
                return {"error": "ERR"}, 404
            db.delete_text_channels(id=channel.id)
        except Exception:
            print_exception()
            return {"error": "ERR"}, 500
        socketio.emit("channel_delete", channel.to_json(), broadcast=True)
        return {"message": "OK"}, 200

    if request.method == "PATCH":
        try:
            channel = db.get_text_channel(id=int(data.get("id")))
            channel.name = data.get("name") or channel.name
            channel.title = data.get("description") or channel.title
            db.modify_text_channel(channel)
        except Exception:
            print_exception()
            return {"error": "ERR"}, 500
        socketio.emit("channel_update", channel.to_json(), broadcast=True)
        return {"message": "OK"}, 200


## ------


@api.route("/messages/<int:channel_id>", methods=("GET",))
@csrf.exempt
def api_message_list(channel_id: int):
    try:
        user = decode_user(request)
    except Exception as error:
        return {"error": str(error)}, 400

    response_messages = []
    messages = db.get_messages(channel_id=channel_id) or []
    if messages:
        for m in messages:
            author = db.get_user(id=m.author_id)
            channel = db.get_text_channel(id=m.channel_id)
            response_messages.append(
                {
                    "message": m.to_json(),
                    "author": author.to_json(),
                    "channel": channel.to_json()
                }
            )
    return {"total_messages": len(messages), "messages_data": response_messages}, 200


@api.route("/message", methods=("GET", "PUT", "DELETE", "PATCH"))
@csrf.exempt
def api_message():
    try:
        user = decode_user(request)
    except Exception as error:
        return {"error": str(error)}, 400

    data = request.json

    if request.method == "GET":
        messages = db.get_messages(id=int(data.get("id")))
        if messages:
            message = messages[0]
            channel = db.get_text_channel(id=message.channel_id)
            author = db.get_user(id=message.author_id)
            data = message.to_json()
            data["channel"] = channel.to_json()
            data["author"] = author.to_json()
            return data, 200
        else:
            return {"error": "NOT FOUND"}, 404

    if request.method == "PUT":
        try:
            message = Message(
                channel_id=int(data.get("channel_id")),
                content=data.get("content"),
                author_id=user.id,
            )
            db.create_message(message)
        except Exception:
            print_exception()
            return {"message": "ERR"}, 500
        channel = db.get_text_channel(id=message.channel_id)
        author = db.get_user(id=message.author_id)
        socketio.emit(
            "message_create",
            {
                "message": message.to_json(),
                "channel": channel.to_json(),
                "author": author.to_json(),
            },
        )
        return {"message": "OK"}, 200

    if request.method == "DELETE":
        try:
            message = db.get_messages(id=int(data.get("id")))[0]
            db.delete_messages(id=int(data.get("id")))
        except Exception:
            print_exception()
            return {"error": "Can not delete message"}, 500
        socketio.emit("message_delete", message.to_json())
        return {"message": "OK"}, 200

    if request.method == "PATCH":
        try:
            message = db.get_messages(id=int(data.get("id")))[0]
            message.content = data.get("content")
            db.modify_message(message)
        except Exception:
            print_exception()
            return {"message": "ERR"}, 500
        socketio.emit("message_update", message.to_json())
        return {"message": "Message edited"}, 200


# ------


@api.route("/login", methods=("POST",))
@csrf.exempt
def login():
    data = request.json
    user = db.get_user(username=data.get("username"))
    if user and user.verify_password(data.get("password")):
        return {
            "user": user.to_json(),
            "token": user.generate_auth_token(),
        }, 200
    else:
        return {"user": None, "token": "Incorrect credentials"}, 401


@api.route("/register", methods=("POST",))
@csrf.exempt
def register_user():
    data = request.json
    user = db.get_user(username=data.get("username"))
    if user:
        return {
            "error": "User is already registered. Try to log in."
        }, 409
    user = User(username=data.get("username"))
    user.password = data.get("password")
    user = db.create_user(user)
    return {
        "user": user.to_json(),
        "token": user.generate_auth_token()
    }, 200


@api.route("/update_user", methods=("POST",))
@csrf.exempt
def update_user():
    # {
    #     "username": "Starlight",
    #     "password": "kapets"
    # }
    data = request.json
    try:
        user = decode_user(request)
    except Exception as error:
        print_exception()
        return {"error": str(error)}, 400
    if db.get_user(username=data.get("username")):
        return {
            "error": "This username is already used. Try to use other username."
        }, 409
    if data.get("username"):
        user.username = data.get("username")
    if data.get("password"):
        if not user.verify_password(data.get("password")):
            user.password = data.get("password")
    user = db.modify_user(user)
    
    return {
        "user": user.to_json(),
        "token": user.generate_auth_token()
    }
  


# ------


@socketio.on("connect")
def on_user_connect(auth):
    user = User.decode_auth_token(auth.get("token"))
    if not auth or not user:
        raise ConnectionError("Incorrect credentials")
    print(f"{user.username} ({user.id}) connected to the party!")

@api.after_request
def add_cors_header(response):
    print(response)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
