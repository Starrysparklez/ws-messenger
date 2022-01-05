from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_compress import Compress
from flask_socketio import SocketIO
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import SECRET_KEY, SQL_URI, SESSION_COOKIE_SAMESITE

socketio = SocketIO()
compress = Compress()
csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "account.login"
login_manager.session_protection = "basic"

def create_flask():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQL_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SESSION_COOKIE_SAMESITE"] = SESSION_COOKIE_SAMESITE

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    login_manager.init_app(app)
    compress.init_app(app)
    socketio.init_app(app)
    csrf.init_app(app)
    db.init_app(app)

    from app.blueprints.account import account
    app.register_blueprint(account, url_prefix="/account")

    from app.blueprints.api import api
    app.register_blueprint(api, url_prefix="/api")

    from app.blueprints.main import main
    app.register_blueprint(main)

    return app, socketio
