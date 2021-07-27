from .auth import auth_bp

def init_app(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
