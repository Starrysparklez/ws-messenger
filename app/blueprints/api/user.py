from traceback import print_exc as print_exception
from flask import request
from app import db, csrf, socketio
from app.miscellaneous import decode_user
from app.models.user import User
from . import api


@api.route("/user", methods=("GET", "PATCH"))
@csrf.exempt
def api_user_info():
    if request.method == "GET":
        try:
            user = decode_user(request)
        except Exception as error:
            print_exception()
            return {
                "status": "ERR",
                "data": str(error)
            }, 400
        return {
            "status": "OK",
            "data": user.to_json()
        }

    if request.method == "PATCH":
        data = request.json
        try:
            user = decode_user(request)
        except Exception as error:
            print_exception()
            return {
                "status": "ERR",
                "data": str(error)
            }, 400
        if db.get_user(username=data.get("username"), discriminator=data.get('discriminator')):
            return {
                "status": "ERR",
                "data": "This username and discriminator is already used."
            }, 409
        if data.get("username"):
            user.username = data.get("username")
        if data.get('discriminator'):
            user.discriminator = data.get('discriminator')
        if data.get("password"):
            if not user.verify_password(data.get("password")):
                user.password = data.get("password")
        user = db.modify_user(user)
        socketio.emit("user_update", user.to_json(), broadcast=True)
        return {
            "status": "OK",
            "data": {
                "user": user.to_json(),
                "token": user.generate_auth_token()
            }
        }


@api.route("/user/login", methods=("POST",))
@csrf.exempt
def login():
    data = request.json
    user = db.get_user(username=data.get("username"))
    if user and user.verify_password(data.get("password")):
        return {
            "status": "OK",
            "data": {
                "user": user.to_json(),
                "token": user.generate_auth_token(),
            }
        }, 200
    else:
        return {
            "status": "ERR",
            "data": "Incorrect credentials"
        }, 401


@api.route("/user/register", methods=("POST",))
@csrf.exempt
def register_user():
    data = request.json
    # user = db.get_user(username=data.get("username"))
    # if user:
    #     return {
    #         "status": "ERR",
    #         "data": "User is already registered. Try to log in."
    #     }, 409
    user = User(username=data.get("username"))
    user.password = data.get("password")
    user = db.create_user(user)
    return {
        "status": "OK",
        "data": {
            "user": user.to_json(),
            "token": user.generate_auth_token()
        }
    }, 200
