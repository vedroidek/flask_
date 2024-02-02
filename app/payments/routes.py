from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.payments import bp
from app.extensions import db
from app.models.all_models import User



@bp.route('/', methods=['GET'])
def index():
    text = 'If you are staff, make log in.'
    return render_template('payments/index.html')


@bp.route('/orders', methods=['GET', 'POST'])
def show_orders():
    # page = db.paginate(db.select(User).order_by(User.join_date))
    d = {num: [num*2, num**2, num+num] for num in range(1, 11)}
    return render_template('payments/orders.html', d=d)