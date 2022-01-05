from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms.fields.simple import PasswordField
from wtforms.validators import EqualTo, Length, InputRequired
from app.models.user import User


class LoginForm(FlaskForm):
    username = StringField("Your nickname", validators=[Length(1, 64), InputRequired()])
    password = PasswordField("Password", validators=[Length(1, 64), InputRequired()])
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    username = StringField("Your nickname", validators=[Length(1, 64), InputRequired()])
    password = PasswordField("Password", validators=[Length(1, 64), InputRequired()])
    password_confirmation = PasswordField("Confirm password", validators=[Length(1, 64), InputRequired(),
                                                                  EqualTo("password", "Password must match.")])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise AttributeError("User with this nickname is already registered.")
