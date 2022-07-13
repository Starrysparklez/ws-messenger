from traceback import print_exc as print_exception
from flask import request
from app import db, csrf, socketio
from app.miscellaneous import decode_user
from . import api
from app.models.message import Message


# receive a list of messages from the text channel
@api.route("/messages/<channel_id>", methods=("GET",))
@csrf.exempt
def api_message_list(channel_id):
    try:
        user = decode_user(request)
        return {
            "status": "OK",
            "data": [x.to_json() for x in db.get_messages(channel_id=channel_id) or []]
        }, 200
    except Exception as error:
        print_exception()
        return {
            "status": "ERR",
            "data": str(error)
        }, 500


# get, create, delete or edit a message
@api.route("/message", methods=("GET", "PUT", "DELETE", "PATCH"))
@csrf.exempt
def api_message():
    try:
        user = decode_user(request)
    except Exception as e:
        return {
            'status': 'ERR',
            'data': str(e)
        }, 400

    data = request.json

    # get information about already existing message
    if request.method == "GET":
        messages = db.get_messages(id=data.get("id"))
        if messages:
            message = messages[0]
            return {
                "status": "OK",
                'data': message.to_json()
            }, 200
        else:
            return {
                "status": "ERR",
                "data": "Messages not found."
            }, 404

    # create a new message
    if request.method == "PUT":
        try:
            message = Message(
                channel_id=int(data.get("channel_id")),
                content=data.get("content"),
                author_id=user.id,
            )
            db.create_message(message)
            socketio.emit("message_create", message.to_json())
            return {
                "status": "OK",
                "data": message.to_json()
            }, 200
        except Exception as e:
            print_exception()
            return {"status": "ERR", "data": str(e)}, 500

    # delete message
    if request.method == "DELETE":
        try:
            messages = db.get_messages(id=data.get('id'))
            if messages:
                message = messages[0]
                db.delete_messages(id=data.get('id'))
                socketio.emit("message_delete", message.to_json())
            else:
                return {
                    "status": "ERR",
                    "data": "Messages not found."
                }, 404
            return {
                "status": "OK",
                'data': message.to_json()
            }, 200
        except Exception as e:
            print_exception()
            return {
                "status": "ERR",
                'data': str(e)
            }, 500

    # edit message
    if request.method == "PATCH":
        try:
            messages = db.get_messages(id=data.get('id'))
            if messages:
                message = messages[0]
                message.content = data.get("content")
                db.modify_message(message)
                socketio.emit("message_update", message.to_json())
                return {
                    "status": "OK",
                    'data': message.to_json()
                }, 200
            else:
                return {
                    "status": 'ERR',
                    'data': 'Messages not found.'
                }, 404
        except Exception as e:
            print_exception()
            return {
                "status": "ERR",
                'data': str(e)
            }, 500
