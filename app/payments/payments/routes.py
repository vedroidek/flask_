from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app.main import bp
from app.extensions import db
from app.models.user import User



@bp.route('/', methods=['GET'])
def index():
    return render_template('payments/orders.html')