from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.payments import bp
from app.extensions import db
from app.models.all_models import User, UserProfile, Order



@bp.route('/', methods=['GET'])
def index():
    text = 'If you are staff, make log in.'
    return render_template('payments/index.html')


@bp.route('/orders', methods=['GET', 'POST'])
def show_orders():
    # page = db.paginate(db.select(User).order_by(User.join_date))
    users = User.query.all()
    statement = db.session.query(User).join(UserProfile).filter(User.id < 10)
    print(statement)
    return render_template('payments/orders.html', users=users)