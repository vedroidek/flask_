import os
from app.extensions import db
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://max:4125@127.0.0.1:5431/flask_app_db',
        # SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        POSTS_PER_PAGE = 10,
        # SQLALCHEMY_ECHO = True,
    )
    
    db.init_app(app=app)
     
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')
    
    from app.seeds import bp as data_bp
    app.register_blueprint(data_bp, url_prefix='/sending_data')
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/user')

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
