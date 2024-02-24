from werkzeug.security import check_password_hash
from flask import request, make_response, render_template, flash, redirect, url_for, session
from sqlalchemy import select
from app.forms import LoginForm
from app import login_manager
from app.auth import bp
from app.extensions import Session
from app.models.all_models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username: str = request.form.get('name')
        password: str = request.form.get('password')
        if all([username, password]):
            with Session() as conn:
                user = conn.scalar(select(User).filter(User.name == username))
                
            password = check_password_hash(user.password, password)
            
            response = make_response(redirect(url_for('home.index')))
            
            response.set_cookie('logged', 'yes', max_age=60*60*24)
            return response
        
        else:
            flash('Name and/or password is invalid.', category='error')
            render_template('auth/login.html')
    return render_template('auth/login.html', form=form)
    # if request.cookies.get('logged') == 'yes':
    #     return redirect('index')
    
    # if request.method == 'POST':
    #     
    
    # return render_template('auth/login.html')


@bp.route('/logout', methods=['GET'])
def logout():
    resp = make_response(redirect(url_for('home.index')))
    resp.set_cookie('logged', 'no', max_age=0)
    return resp