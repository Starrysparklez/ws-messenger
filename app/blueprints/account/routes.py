from flask import Blueprint, flash, render_template, redirect, request, make_response
from flask_login import login_user, logout_user, current_user
from .forms import LoginForm, RegisterForm
from app.models.user import User
from app import db

account = Blueprint('account', __name__)

@account.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, True)
            response = make_response(redirect("/channels/1"))
            response.set_cookie("mysupersecrettoken", user.generate_auth_token())
            return response
    return render_template("account/login.html", form=form)

@account.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm(request.form)
    try:
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            login_user(user, True)
            flash(f"Welcome, {user.username}!", "success")
            response = make_response(redirect("/channels/1"))
            response.set_cookie("mysupersecrettoken", user.generate_auth_token())
            return response
    except AttributeError:
        # is already registered
        pass
    return render_template("account/register.html", form=form)

@account.route("/logout", methods=("GET",))
def logout():
    logout_user()
    response = make_response(redirect("/account/login"))
    response.delete_cookie("mysupersecrettoken")
    return response
