from .order import order_bp

def init_app(app):
    app.register_blueprint(order_bp, url_prefix='/order')
