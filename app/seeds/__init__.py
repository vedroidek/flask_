from flask import Blueprint

bp = Blueprint('sending_data', __name__, url_prefix='/sending_data')


from app.seeds import routes