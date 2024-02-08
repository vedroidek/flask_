from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import select, join
from werkzeug.security import check_password_hash
from app.payments import bp
from app.extensions import db
from app.models.all_models import User, UserProfile, Order



@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    text = 'If you are staff, make log in.'
    return render_template('payments/index.html')


@bp.route('/orders', methods=['GET', 'POST'])
def show_orders():
    if request.method == 'POST':
        page = int(request.form['num_page'])
    else:
        page = request.args.get('page', 1, type=int)
    
    all_rows = Order.query.count()
    per_page: int = 20
    start: int = (page -1) * per_page
    end: int = start + per_page
    total_pages: int = (all_rows + per_page - 1) // per_page
    items_on_page: int = Order.query.order_by(Order.total_cost.asc()).all()[start:end]
        
    return render_template('payments/orders.html', items_on_page=items_on_page,
                           total_pages=total_pages, page=page, all_rows=all_rows)
    

@bp.route('/detail', methods=['GET'])
def order_detail():
    user_id = request.args.get('user_id')
    user = db.session.execute(select(User).where(User.id == user_id)).first()
    print(user)
    stmt = db.session.execute(select(User.name, User.email, Order.status, Order.total_cost) \
                              .join(User).where(User.id == Order.user_id). \
                                order_by(User.name)).first()
    
    return render_template('payments/detail.html', stmt=stmt)
    