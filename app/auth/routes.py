from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, make_response, render_template, flash, redirect, url_for, session
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError
from app.redis_cli import redis_client as r
from app.forms import LoginForm
from app.auth import bp
from app.extensions import Session
from app.models.all_models import User


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        email = request.form['email']
        error = None
        
        password=generate_password_hash(password, method='pbkdf2', salt_length=16)

        if not all([username, password, email]):
            flash('All fields are required.')
            error = 'All fields are required.'
        
        if error is None:
            try:
                user = (insert(User).values(name=username, password=password, email=email))
                with Session.begin() as conn:
                    conn.execute(user)
                    conn.commit()
            except IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('auth.index'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """ View for user login. """
    form = LoginForm()
    username: str = request.form.get('name')
    password: str = request.form.get('password')
    if form.validate_on_submit():
        with Session() as conn:
            user: str = conn.scalar(select(User).filter(User.name == username))
            
        password = check_password_hash(user.password, password)
        
        r.set(f'is_logged:{user.name}', 'yes', ex=3600)
        return redirect(url_for('home.index'))
        
    else:
        flash('Name and/or password is invalid.', category='error')
        render_template('auth/login.html')
    return render_template('auth/login.html', form=form)


@bp.route('/logout', methods=['GET'])
def logout():
    r.set(name=f'is_logged:{User.id}', value='no')
    return redirect(url_for('home.index'))