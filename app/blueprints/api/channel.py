from traceback import print_exc as print_exception
from flask import request
from app import db, csrf, socketio
from app.miscellaneous import decode_user
from . import api
from app.models.channel import Channel


@api.route("/channels", methods=("GET",))
@csrf.exempt
def api_channel_list():
    try:
        user = decode_user(request)
    except Exception as e:
        print_exception()
        return {
            "status": "ERR",
            "data": str(e)
        }, 400

    channels = db.get_all_channels() or []
    return {
        "status": "OK",
        "data": [x.to_json() for x in channels],
    }, 200


@api.route("/channel", methods=("GET", "PUT", "DELETE", "PATCH"))
@csrf.exempt
def api_channel():
    try:
        user = decode_user(request)
    except Exception as e:
        print_exception()
        return {
            "status": "ERR",
            "data": str(e)
        }, 400

    data = request.json

    if request.method == "GET":
        channel = db.get_channel(id=data.get('id'))
        if channel:
            return {
                "status": "OK",
                "data": channel.to_json()
            }, 200
        else:
            return {
                "status": "ERR",
                "data": "Channel not found."
            }, 404

    if request.method == "PUT":
        try:
            channel = Channel(
                name=data.get("name"), topic=data.get("topic"), type=data.get('type')
            )
            db.create_channel(channel)
            socketio.emit("channel_create", channel.to_json(), broadcast=True)
            return {
                "status": "OK",
                "data": channel.to_json()
            }, 200
        except Exception as e:
            print_exception()
            return {
                "status": "ERR",
                "data": str(e)
            }, 500

    if request.method == "DELETE":
        try:
            channel = db.get_channel(id=data.get('id'))
            if not channel:
                return {
                    "status": "ERR",
                    "data": "Channel not found."
                }, 404
            db.delete_channels(id=channel.id)
            socketio.emit("channel_delete", channel.to_json(), broadcast=True)
            return {
                "status": "OK",
                "data": channel.to_json()
            }, 200
        except Exception as e:
            print_exception()
            return {
                "status": "ERR",
                "data": str(e)
            }, 500

    if request.method == "PATCH":
        try:
            channel = db.get_channel(id=data.get('id'))
            if not channel:
                return {
                    "status": "ERR",
                    'data': 'Channel not found.'
                }, 404
            channel.name = data.get("name") or channel.name
            channel.topic = data.get("topic") or channel.topic
            db.modify_channel(channel)
            socketio.emit("channel_update", channel.to_json(), broadcast=True)
            return {
                "status": "OK",
                "data": channel.to_json()
            }, 200
        except Exception as e:
            print_exception()
            return {
                "status": "ERR",
                "data": str(e)
            }, 500
