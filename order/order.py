from flask import Blueprint

from auth.myJwt import jwt_required

order_bp = Blueprint("order", __name__)

@order_bp.route('/tealist', methods=['GET', 'POST'])
def tea_list():
    pass