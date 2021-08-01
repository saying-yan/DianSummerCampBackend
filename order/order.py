from flask import Blueprint, json, request

from ..auth.myJwt import jwt_required
from ..modules import ProductCategory, Products

order_bp = Blueprint("order", __name__)

@order_bp.route('/getProductListInfo', methods=['GET', 'POST'])
def tea_list():
    productLists = ProductCategory.query.all()
    return json.jsonify(
        status="success",
        data=[i.serialize for i in productLists]
    )