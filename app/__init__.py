'''docs'''

import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config



db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)


def register_blueprints(app):
    from .view.users import users
    app.register_blueprint(users, url_prefix='/api')


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:

            print('> Error: DBMS Exception: ' + str(e) )


    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove() 



def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    from app.model import data_model
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
   

    return app




