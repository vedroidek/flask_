from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app.main import bp
from app.extensions import engine, Session
from app.models.all_models import User


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


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
                return redirect(url_for('home.index'))

        flash(error)

    return render_template('register.html')