from typing import Type
from http import HTTPStatus as status
from flask import render_template, request
from flask.views import MethodView
from sqlalchemy import select
from werkzeug.security import generate_password_hash
import app
from app.extensions import db
from app.users import bp
from app.models.all_models import User, UserProfile


def get_user_id(id: int, orm_model: Type[User], session=db.session):
    """ Get user from DB if exist. """
    with db.session() as session:
        user = session.execute(select(orm_model).where(User.id == id)).first()
        if not user:
            return status.NOT_FOUND
        return user[0]


class UserView(MethodView):
    
    def get(self, user_id):
        with db.session() as session:
            user = get_user_id(user_id, User, session)
            return user
    
    def post(self, id: int, name: str, email: str, password: str):
        with db.session() as session:
            user = get_user_id(id, User, session)
            if not user:
                return status.NOT_FOUND
            elif user.email == email:
                return status.CONFLICT
            try:
                password = generate_password_hash(password, method='pbkdf2', salt_length=16)
                new_user = User(name=name, email=email, password=password)
                session.add(new_user)
                session.commit()
            except db.IntegrityError:
                session.rollback()
                return status.CONFLICT
            return status.OK
    
    def patch(self, id: int, name: str=None, email: str=None, password: str=None):
        with db.session() as session:
            u = get_user_id(id, User, session)
            if not u:
                return status.NOT_FOUND
            try:
                password = generate_password_hash(password, method='pbkdf2', salt_length=16)
                user = User(name=name, email=email, password=password)
                session.add(user)
                session.commit()
            except db.IntegrityError:
                session.rollback()
                return status.CONFLICT
            return status.OK
    
    def delete(self, id: int):
        with db.session() as session:
            user = get_user_id(id, User, session)
            if not user:
                return status.NOT_FOUND
            try:
                session.delete(user)
                session.commit()
            except db.IntegrityError:
                session.rollback()
                return status.CONFLICT
            return status.OK


@bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('users/index.html')


@bp.route('/profile/')
def user_profile():
    return render_template('users/profile')


@bp.route('/user_detail', methods=['GET'])
def user_detail() -> str:
    user_id = request.args.get('user')
    user = get_user_id(user_id, User, db.session)
    return render_template('users/user_detail.html', user=user)


app.add_url_rule('/user/<int:user_id>/', view_func=UserView.as_view('users_get'),
                 methods=['GET', 'PATCH', 'DELETE'])
