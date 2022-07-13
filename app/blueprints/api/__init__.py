from flask import Blueprint


api = Blueprint("api", __name__)

@api.after_request
def add_cors_header(response):
    print(response)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    return response

from .message import *
from .channel import *
from .user import *
from .socket import *
