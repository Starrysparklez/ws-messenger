import os
import psycopg2
from flask import Flask
from flask_compress import Compress
from flask_socketio import SocketIO
from flask_wtf import CSRFProtect
from app.db import Database
from config import (
    SECRET_KEY,
    SESSION_COOKIE_SAMESITE,
    PSQL_DBNAME,
    PSQL_HOST,
    PSQL_PORT,
    PSQL_USER,
    PSQL_PASSWD,
)

socketio = SocketIO()
compress = Compress()
csrf = CSRFProtect()
psql_connection = psycopg2.connect(
    host=PSQL_HOST,
    port=PSQL_PORT,
    dbname=PSQL_DBNAME,
    user=PSQL_USER,
    password=PSQL_PASSWD,
)
db = Database(psql_connection)


def create_flask():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SESSION_COOKIE_SAMESITE"] = SESSION_COOKIE_SAMESITE

    compress.init_app(app)
    socketio.init_app(app)
    csrf.init_app(app)

    from app.blueprints.api import api

    app.register_blueprint(api)

    return app, socketio


for directory in (
    "app/static",
    "app/static/usercontent",
    "app/static/usercontent/avatars",
):
    if not os.path.exists(directory):
        os.mkdir(directory)
