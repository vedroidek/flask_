from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from sqlalchemy import select
from app.models.all_models import User
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, InputRequired


class LoginForm(FlaskForm):
            
    name = StringField('Full Name: ', validators=[InputRequired(), DataRequired(), Length(min=3, max=64)],
                       render_kw={'placeholder': 'username'})
    pswd = PasswordField('Password', [InputRequired(), DataRequired(), Length(min=6, max=128)],
                         render_kw={'placeholder': 'password'})
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('LogIn')
    
    def validate_username(self, name):
        existing_username = select(User).filter_by(username=name.data)
        if existing_username:
            raise ValidationError('That username already exists.')
    
    
class RegisterForm(FlaskForm):
    
    name = StringField('Full Name: ', validators=[InputRequired(), DataRequired(), Length(min=3, max=64)],
                       render_kw={'placeholder': 'username'})
    email = StringField('Email: ', validators=[InputRequired(), Email()],
                        render_kw={'placeholder': 'email'})
    pswd = PasswordField('Password', [InputRequired(), DataRequired(), Length(min=6, max=128)],
                         render_kw={'placeholder': 'password'})
    submit = SubmitField('Register')