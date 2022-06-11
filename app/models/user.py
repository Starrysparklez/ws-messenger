import typing
from datetime import datetime
from jwt import encode, decode
from werkzeug.security import check_password_hash, generate_password_hash
from config import SECRET_KEY, base_url
from PIL import Image


class User:
    def __init__(self, **kwargs):
        """Init a new User object.

        Parameters
        ==========
        id: int
            User ID
        username: str
            User name
        avatar_hash: str
            Hash of the user's avatar
        password_hash: str
            Hash of the user's password
        created_at: datetime.datetime
            Account creation timestamp
        locale: str
            User's locale
        """
        self.id: int = kwargs.pop("id", None)
        self.username: str = kwargs.pop("username", None)
        self.avatar_hash: str = kwargs.pop("avatar_hash", None)
        self.password_hash: str = kwargs.pop("password_hash", None)
        self.created_at: datetime = kwargs.pop("created_at", None)
        self.locale: str = kwargs.pop("locale", None)

    def to_json(self) -> typing.Dict:
        """Convert to json."""
        return {
            "id": str(self.id),
            "username": self.username,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.timestamp(),
            "locale": self.locale,
        }

    @property
    def password(self) -> None:
        raise AttributeError("Password is not readable attribute.")

    @password.setter
    def password(self, new_password):
        self.password_hash = generate_password_hash(new_password)

    def verify_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def avatar_url(self) -> str:
        return f"{base_url}/static/usercontent/avatar_{self.id}.jpg"

    @avatar_url.setter
    def avatar_url(self, new_avatar: bytes):
        im = Image.open(new_avatar)
        im_new = im.resize((256, 256), Image.BILINEAR)
        im_new.save(f"app/static/usercontent/avatar_{self.id}.jpg", format="jpeg")

    def generate_auth_token(self) -> str:
        payload = {"uid": self.id, "phs": self.password_hash}
        return encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_auth_token(token) -> dict:
        try:
            payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            raise RuntimeError("Unable to decode authentication token.")
        return {"id": payload.get("uid"), "password_hash": payload.get("phs")}
