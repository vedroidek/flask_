from flask import Blueprint

bp = Blueprint('home', __name__)


from app.main import routes