from random import uniform, choice
from flask import request, redirect, url_for, render_template, flash
from app.seeds import bp
from app.extensions import db
from app.models.all_models import User, Order, OrderStatus
from faker import Faker


@bp.route('/', methods=['GET', 'POST'])
def send_():
    if request.method == 'POST':
        answer = request.form['add-data']
        users = []
        if answer == 'Yes':
            fk = Faker()
            try:
                for _ in range(100):
                    user = User(name=fk.name(),
                                password=hash(fk.name()),
                                email=fk.email())
                    db.session.add(user)
                    users.append(user)
                db.session.commit()
                
                last_100_id = list(map(lambda x: x.id, users))
                
                for _ in range(5000):
                    order = Order(total_cost=round(uniform(0.0, 10000.0), 3),
                                  user_id=choice(last_100_id),
                                  status=choice(dir(OrderStatus)[:3]))
                    db.session.add(order)
                db.session.commit()
                    
                flash('Data sent.', category='info')
            except db.IntegrityError:
                db.session.rollback()
                return '<h1>FAIL</h1>'
        elif answer == 'Delete all':
            try:
                db.session.query(Order).delete()
                db.session.query(User).delete()
                db.session.commit()
                flash('All rows removed.', category='info')
            except db.IntegrityError:
                db.session.rollback()
        else:
            return redirect(url_for('home.index'))
    return render_template('seeds/index.html')