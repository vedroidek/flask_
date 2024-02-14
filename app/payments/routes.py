from flask import render_template, request
from sqlalchemy import select, func
from app.payments import bp
from app.extensions import Session
from app.models.all_models import Order



@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    text: str = 'If you are staff, make log in.'
    return render_template('payments/index.html', text=text)


@bp.route('/orders', methods=['GET', 'POST'])
def show_orders():
    if request.method == 'POST':
        page = int(request.form['num_page'])
    else:
        page = request.args.get('page', 1, type=int)
    
    all_rows = Session().query(Order).count()
    per_page: int = 20
    start: int = (page - 1) * per_page
    end: int = start + per_page
    total_pages: int = (all_rows + per_page - 1) // per_page
    items_on_page: int = Session().query(Order).all()[start:end]
        
    return render_template('payments/orders.html', items_on_page=items_on_page,
                           total_pages=total_pages, page=page, all_rows=all_rows)
    
    
@bp.route('/detail', methods=['GET'])
def order_detail():
    order_id = request.args.get('order')
    with Session() as conn:
        order = conn.get(Order, order_id)
    return render_template('payments/detail.html', order=order)


