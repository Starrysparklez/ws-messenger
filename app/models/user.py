import typing, io
from datetime import datetime
from jwt import encode, decode
from werkzeug.security import check_password_hash, generate_password_hash
from config import base_url
from PIL import Image

with io.open("keypair/public.pub", "r") as pub:
    public_key = pub.read()
with io.open("keypair/private", "r") as priv:
    private_key = priv.read()

class User:
    def __init__(self, **kwargs):
        """Init a new User object.

        Parameters
        ==========
        id: str
            User ID
        username: str
            User name
        role: int
            User's role
        password_hash: str
            Hash of the user's password
        created_at: datetime.datetime
            Account creation timestamp
        locale: str
            User's locale
        discriminator: str
            User's discriminator number.
        """
        self.id: str = kwargs.pop("id", None)
        self.username: str = kwargs.pop("username", None)
        self.role: str = kwargs.pop("role", 'user')
        self.password_hash: str = kwargs.pop("password_hash", None)
        self.created_at: datetime = kwargs.pop("created_at", datetime.now())
        self.locale: str = kwargs.pop("locale", None)
        self.discriminator: str = kwargs.pop('discriminator', '0000')

    def to_json(self) -> typing.Dict:
        """Convert to json."""
        return {
            "id": self.id,
            "role": self.role,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at.strftime("%c"),
            "locale": self.locale,
            'discriminator': self.discriminator
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
        return f"{base_url}/static/usercontent/avatars/{self.id}.jpg"

    @avatar_url.setter
    def avatar_url(self, new_avatar: bytes):
        im = Image.open(new_avatar)
        im_new = im.resize((256, 256), Image.BILINEAR)
        im_new.save(f"app/static/usercontent/avatars/{self.id}.jpg", format="jpeg")

    def generate_auth_token(self) -> str:
        payload = {"uid": self.id, "phs": self.password_hash}
        return encode(payload, private_key, algorithm="RS256").decode('utf-8')

    @staticmethod
    def decode_auth_token(token) -> dict:
        try:
            payload = decode(token, public_key, algorithms=["RS256"])
        except:
            raise RuntimeError("Unable to decode authentication token.")
        return {"id": payload.get("uid"), "password_hash": payload.get("phs")}
