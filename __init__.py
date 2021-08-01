from flask import Flask

from .settings import Config
from .modules import db
from . import auth, order

# 支持跨域
def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.headers['Access-Control-Allow-Credentials'] = 'true'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, authentication'
    return resp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config.update(use_reloader=False)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    auth.init_app(app)
    order.init_app(app)

    app.after_request(after_request)

    return app
