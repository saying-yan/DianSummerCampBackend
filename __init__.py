from flask import Flask

from .settings import Config
from .modules import db
from . import auth

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    auth.init_app(app)

    return app
