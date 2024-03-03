from flask import render_template, request
from app.main import bp


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
