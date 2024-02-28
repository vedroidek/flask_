from flask import render_template
from app.main import bp


@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')
