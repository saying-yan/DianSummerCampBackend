from .auth import auth_bp
from ..modules import UserInfo

def init_app(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
