from flask import Flask
from config import Config
from app.extensions import DSN, create_engine, declarative_base, sessionmaker


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # initial DB
    engine = create_engine(DSN)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)

    # register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
