from app.blueprints.account.forms import LoginForm
from traceback import print_exc as print_exception
from app.models.channel import TextChannel
from app.models.message import Message
from flask import Blueprint, request
from flask_login import login_user
from flask_socketio import emit, join_room, leave_room, ConnectionRefusedError as ConnectionError
from app.models.user import User
from app import db, csrf, socketio
from copy import copy

api = Blueprint("channels", __name__)

# ------

@api.route("/channels", methods=("GET",))
@csrf.exempt
def api_channel_list():
    user = User.decode_auth_token(request.headers.get("Authorization"))
    if not request.headers.get("Authorization") or not user:
        return {
            "error": "Incorrect credentials"
        }, 401

    channels = TextChannel.query.all()
    return {
        "total_channels": len(channels),
        "channels_data": [x.to_json() for x in channels]
    }, 200

@api.route("/channel", methods=("GET", "PUT", "DELETE"))
@csrf.exempt
def api_channel():
    data = request.json

    user = User.decode_auth_token(request.headers.get("Authorization"))
    if not request.headers.get("Authorization") or not user:
        return {
            "error": "Incorrect credentials"
        }, 401

    if request.method == "GET":
        channel = TextChannel.query.filter_by(id=data.get("id")).first()
        if channel:
            return channel.to_json(), 200
        return {
            "error": f"Channel with ID {data.get('id')} does not exists"
        }, 404
    if request.method == "PUT":
        try:
            channel = TextChannel(name=data.get("name"), title=data.get("title"))
            db.session.add(channel)
            db.session.commit()
        except Exception:
            print_exception()
            return {
                "error": "Can not create channel"
            }, 500
        socketio.emit("channel_create", {
            "id": channel.id,
            "name": channel.name,
            "title": channel.title
        }, broadcast=True)
        return channel.to_json(), 200
    if request.method == "DELETE":
        try:
            channel = TextChannel.query.filter_by(id=data.get("id")).first()
            channel.delete()
            db.session.commit()
        except Exception:
            print_exception()
            return {
                "error": "Can not delete channel"
            }, 500
        socketio.emit("channel_delete", {
            "id": channel.id,
            "name": channel.name,
            "title": channel.title
        }, broadcast=True)
        return {
            "message": "Channel deleted"
        }, 200
    if request.method == "PATCH":
        try:
            channel = TextChannel.query.filter_by(id=data.get("id"))
            old_channel = copy(channel)
            channel.name = data.get("name") or channel.name
            channel.title = data.get("title") or channel.title
            db.session.commit()
        except Exception:
            print_exception()
            return {
                "error": "Can not edit channel"
            }, 500
        socketio.emit("channel_update", {
            "old_channel": {
                "id": old_channel.id,
                "name": old_channel.name,
                "title": old_channel.title
            },
            "new_channel": {
                "id": channel.id,
                "name": channel.name,
                "title": channel.title
            }
        }, broadcast=True)
        return {
            "message": "Channel edited"
        }, 200

## ------

@api.route("/messages/<int:channel_id>", methods=("GET",))
@csrf.exempt
def api_message_list(channel_id: int):
    user = User.decode_auth_token(request.headers.get("Authorization"))
    if not request.headers.get("Authorization") or not user:
        return {
            "error": "Incorrect credentials"
        }, 401

    response_messages = []
    messages = Message.query.filter_by(channel_id=channel_id).all()
    for m in messages:
        channel = TextChannel.query.filter_by(id=m.channel_id).first()
        author = User.query.filter_by(id=m.author_id).first()
        response_messages.append({
            "id": m.id,
            "content": m.content,
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "title": channel.title
            },
            "author": {
                "id": author.id,
                "username": author.username
            }
        })
    return {
        "total_messages": len(messages),
        "messages_data": response_messages
    }, 200

@api.route("/message", methods=("GET", "PUT", "DELETE", "PATCH"))
@csrf.exempt
def api_message():
    data = request.json

    user = User.decode_auth_token(request.headers.get("Authorization"))
    if not request.headers.get("Authorization") or not user:
        return {
            "error": "Incorrect credentials"
        }, 401

    if request.method == "GET":
        message = Message.query.filter_by(id=data.get("id")).first()
        if message:
            channel = TextChannel.query.filter_by(id=message.channel_id)
            author = User.query.filter_by(id=message.author_id)
            return {
                "id": message.id,
                "content": message.content,
                "channel": {
                    "id": channel.id,
                    "name": channel.name,
                    "title": channel.title
                },
                "author": {
                    "id": author.id,
                    "username": author.username
                }
            }, 200
        else:
            return {
                "error": f"Message with ID {data.get('id')} does not exists"
            }, 404
    if request.method == "PUT":
        try:
            message = Message(
                channel_id=data.get("channel_id"),
                content=data.get("content"),
                author_id=user.id
            )
            db.session.add(message)
            db.session.commit()
        except Exception:
            print_exception()
            return {
                "error": "Can not create message"
            }, 500
        channel = TextChannel.query.filter_by(id=message.channel_id).first()
        author = User.query.filter_by(id=message.author_id).first()
        socketio.emit("message_create", {
            "id": message.id,
            "content": message.content,
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "title": channel.title
            },
            "author": {
                "id": author.id,
                "username": author.username
            }
        }, to=channel.id)
        return {
            "message": "Message created"
        }, 200
    if request.method == "DELETE":
        try:
            message = Message.query.filter_by(id=data.get("id")).first()
            message.delete()
            db.session.commit()
        except Exception:
            print_exception()
            return {
                "error": "Can not delete message"
            }, 500
        channel = TextChannel.query.filter_by(id=message.channel_id).first()
        author = User.query.filter_by(id=message.author_id).first()
        socketio.emit("message_delete", {
            "id": message.id,
            "content": message.content,
            "channel": {
                "id": channel.id,
                "name": channel.name,
                "title": channel.title
            },
            "author": {
                "id": author.id,
                "username": author.username
            }
        }, to=channel.id)
        return {
            "message": "Message deleted"
        }, 200
    if request.method == "PATCH":
        try:
            message = Message.query.filter_by(id=data.get("id")).first()
            old_message = copy(message)
            message.content = data.get("content")
            db.session.commit()
        except Exception:
            print_exception()
            return {
                "error": "Can not edit message"
            }, 500
        channel = TextChannel.query.filter_by(id=message.channel_id).first()
        author = User.query.filter_by(id=message.author_id).first()
        socketio.emit("message_update", {
            "before": {
                "id": old_message.id,
                "content": old_message.content,
                "channel": {
                    "id": channel.id,
                    "name": channel.name,
                    "title": channel.title
                },
                "author": {
                    "id": author.id,
                    "username": author.username
                }
            },
            "after": {
                "id": message.id,
                "content": old_message.content,
                "channel": {
                    "id": channel.id,
                    "name": channel.name,
                    "title": channel.title
                },
                "author": {
                    "id": author.id,
                    "username": author.username
                }
            }
        }, to=channel.id)
        return {
            "message": "Message edited"
        }, 200

# ------

@api.route("/login", methods=("POST",))
@csrf.exempt
def validate_account_login_and_password_to_retrieve_auth_token_for_this_account():
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.verify_password(data.get("password")):
        login_user(user, True)
        return {
            "user": {
                "id": user.id,
                "username": user.username
            },
            "token": user.generate_auth_token()
        }, 200
    else:
        return {
            "user": None,
            "token": "Incorrect credentials"
        }, 401

# ------

@socketio.on("connect")
def on_user_connect(auth):
    if not auth or not User.decode_auth_token(auth.get("token")):
        raise ConnectionError("Incorrect credentials")

@socketio.on("join")
def join_channel(data):
    if not data or not data.get("token"):
        raise ConnectionError("You should provide authorization token")
    user = User.decode_auth_token(data.get("token"))
    if not user:
        raise ConnectionError("Invalid credentials")

    join_room(int(data.get("channelId")))
    channel = TextChannel.query.filter_by(id=data.get("channelId")).first()
    socketio.emit("message_create", {
        "id": None,
        "content": f"User @{user.username} joined this channel!",
        "channel": {
            "id": channel.id,
            "name": channel.name,
            "title": channel.title
        },
        "author": {}
    }, to=channel.id)
