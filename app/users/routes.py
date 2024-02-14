from typing import Type
from http import HTTPStatus as status
from flask import render_template, request
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app.extensions import Session
from app.users import bp
from app.models.all_models import User


def get_user_id(id: int, orm_model: Type[User], session=Session):
    """ Get user from DB if exist. """
    with Session() as session:
        user = session.get(User, id)
    if not user:
        return status.NOT_FOUND
    return user


class UserView(MethodView):
    
    @bp.route('/<int:user_id>')
    def get(self, user_id):
        with Session() as session:
            user = get_user_id(user_id, User, Session)
            return user
    
    @bp.route('/')
    def post(self, user_id: int, name: str, email: str, password: str):
        user = get_user_id(user_id, User, Session)
        if user or user.email == email:
            return status.CONFLICT
        password = generate_password_hash(password, method='pbkdf2', salt_length=16)
        with Session.begin() as session:
            try:                
                new_user = User(name=name, email=email, password=password)
                session.add(new_user)
                session.commit()
            except IntegrityError:
                session.rollback()
                return status.CONFLICT
            return status.OK
    
    @bp.route('/<int:user_id>')
    def patch(self, user_id: int, name: str=None, email: str=None, password: str=None):
        u = get_user_id(user_id, User, Session)
        if not u:
            return status.NOT_FOUND
        with Session.begin() as session:
            try:
                password = generate_password_hash(password, method='pbkdf2', salt_length=16)
                user = User(name=name, email=email, password=password)
                session.add(user)
                session.commit()
            except IntegrityError:
                session.rollback()
                return status.CONFLICT
            return status.OK
    
    @bp.route('/<int:user_id>')
    def delete(self, user_id: int):
        user = get_user_id(user_id, User, Session)
        if not user:
            return status.NOT_FOUND
        with Session() as session:
            try:
                session.delete(user)
                session.commit()
            except IntegrityError:
                session.rollback()
                return status.CONFLICT
            return status.OK


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('users/index.html')


@bp.route('/user_detail', methods=['GET'])
def user_detail():
    user_id = request.args.get('user_id')
    user = get_user_id(user_id, User, Session)
    return render_template('users/user_detail.html', user=user)
