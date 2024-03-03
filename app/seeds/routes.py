from random import uniform, choice
from flask import request, redirect, url_for, render_template, flash
from sqlalchemy.exc import IntegrityError
from flask_login import login_required
from app.seeds import bp
from app.extensions import Session
from app.models.all_models import User, Order, OrderStatus
from faker import Faker


@bp.route('/', methods=['GET', 'POST'])
@login_required
def create_test_data():
    if request.method == 'POST':
        answer = request.form.get('add-data')
        if answer == 'Yes':
            users = []
            with Session() as session:
                try:
                    create_test_users(session, count=100, users=users)
                    last_100_id = list(map(lambda x: x.id, users))
                    
                    create_test_orders(session, count=5000, ids=last_100_id)
                    flash('Data send.', category='info')
                except IntegrityError:
                    session.rollback()
                
        elif answer == 'Delete all':
            with Session.begin() as session:
                try:
                    session.query(Order).delete()
                    session.query(User).delete()
                    session.commit()
                    flash('All rows removed.', category='info')
                except IntegrityError:
                    session.rollback()
                    return '<h1>FAIL</h1>'
        else:
            return redirect(url_for('home.index'))
    return render_template('seeds/index.html')


def create_test_users(session, count: int, users: list):
    fk = Faker()
    for _ in range(count):
        user = User(name=fk.name(),
                    password=hash(fk.name()),
                    email=fk.email())
        session.add(user)
        users.append(user)
    session.commit()


def create_test_orders(session, count: int, ids: list):
    for _ in range(count):
        order = Order(total_cost=round(uniform(0.0, 10000.0), 3),
                        user_id=choice(ids),
                        status=choice(dir(OrderStatus)[:3]))
        session.add(order)
    session.commit()