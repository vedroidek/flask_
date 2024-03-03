from typing import Type
from http import HTTPStatus as status
from flask import render_template, request, g
from flask.views import MethodView
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app.extensions import Session
from app.users import bp
from app.models.all_models import User


def get_user(id: int, orm_model: Type[User], session=Session):
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
            user = session.get(User, user_id)
            return user
    
    @bp.route('/')
    def post(self, name: str=None, email: str=None, password: str=None):
        email_exists = select(User.email).filter(email=email)
        if email_exists:
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
        u = get_user(user_id, User, Session)
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
        user = get_user(user_id, User, Session)
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


@bp.route('/', methods=['GET'])
@bp.route('/<int:user_id>', methods=['GET', 'POST'])
def index(user_id: int = None):
    user = get_user(user_id, User, Session)
    return render_template('users/index.html')


@bp.route('/user_detail', methods=['GET'])
def user_detail():
    user_id = request.args.get('user_id')
    user = get_user(user_id, User, Session)
    if request.cookies.get('logged'):
        log = request.cookies.get('logged')
    return render_template('users/user_detail.html', user=user)
