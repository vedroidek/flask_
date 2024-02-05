from flask import request, redirect, url_for, render_template, flash
from app.seeds import bp
from app.extensions import db
from app.models.all_models import User
from faker import Faker


@bp.route('/', methods=['GET', 'POST'])
def send_():
    if request.method == 'POST':
        answer = request.form['add-data']
        if answer == 'Yes':
            fk = Faker()
            try:
                for _ in range(100):
                    user = User(name=fk.name(),
                                password=hash(fk.name()),
                                email=fk.email())
                    db.session.add(user)
                db.session.commit()
                flash('Data sent.', category='info')
            except db.IntegrityError:
                db.session.rollback()
                return '<h1>FAIL</h1>'
        elif answer == 'Delete all':
            try:
                db.session.query(User).delete()
                db.session.commit()
            except db.IntegrityError:
                db.session.rollback()
        else:
            return redirect(url_for('home.index'))
    return render_template('seeds/index.html')