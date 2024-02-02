from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.main import bp
from app.extensions import db
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

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(name=username,
                            password=password,
                            email=email)
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('home.index'))

        flash(error)

    return render_template('register.html')