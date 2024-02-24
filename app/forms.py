from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
            
    name = StringField('Full Name: ', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email: ', validators=[Email()])
    pswd = PasswordField('Password', [DataRequired(), Length(min=6, max=128)])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('LogIn')