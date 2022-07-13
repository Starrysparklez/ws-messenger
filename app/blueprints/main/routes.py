from flask import Blueprint, request, render_template

general = Blueprint("main", __name__)

@general.route("/", methods=("GET",))
def index():
    return "Hello World! You're on the main page. <a href='/chat'>Go to the messenger demo.</a>"

@general.route("/chat", methods=("GET",))
def chat_route():
    return render_template("chat.html")
