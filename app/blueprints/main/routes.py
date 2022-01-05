from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

@main.route("/channels", methods=("GET",))
@main.route("/channels/<int:channel_id>", methods=("GET",))
@login_required
def channels(channel_id=None):
    print(current_user.username)
    if channel_id:
        return render_template("/chatroom/chat.html")
    return render_template("/chatroom/start.html")
