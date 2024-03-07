from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, render_template, flash, redirect, url_for, make_response, session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm, RegisterForm
from app.auth import bp
from app.extensions import Session
from app.models.all_models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    error = None
    if form.validate_on_submit() and form.check_pswds():
        username = form.name.data
        password = form.pswd.data
        email = form.email.data
        
        is_exsist_email = Session().scalar(select(User).filter(User.email == email))
        if is_exsist_email:
            error = 'This email already exsists.'
        
        if error is None:
            password=generate_password_hash(password, method='pbkdf2', salt_length=16)
            with Session() as conn:
                try:
                    stmt = insert(User).values(name=username, password=password, email=email)
                    conn.execute(stmt)
                    conn.commit
                except IntegrityError:
                    error = f"User {username} is already registered."
                    conn.rollback()
        else:
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """ View for user login. """
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        with Session() as conn:
            user = conn.scalar(select(User).filter(User.name == form.name.data))
            
        if user and check_password_hash(user.password, form.pswd.data):
            login_user(user=user, remember=form.remember.data, force=True)
        
        if previous_page := request.args.get('next'):
            response = make_response(redirect(previous_page))
        else:
            response = make_response(render_template('index.html'))
            
        return response
        
    else:
        error = 'Name and/or password is invalid.'
        flash(error, category='error')
        render_template('auth/login.html', form=form)
    return render_template('auth/login.html', form=form)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.index'))
