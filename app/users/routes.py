from flask import render_template
from sqlalchemy import select
from app.users import bp
from app.extensions import Session
from app.models.user import User, UserProfile


@bp.route('/', methods=['GET', 'POST'])
def index():
    with Session() as s:
        statement = s.query(User).first()
    return render_template('users/index.html', statement=statement)


@bp.route('/register', methods=['GET', 'POST'])
def user_register():
    pass


@bp.route('/profile/')
def user_profile():
    return render_template('users/profile')
