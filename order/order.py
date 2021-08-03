from flask import Blueprint, json, request

from ..auth.myJwt import jwt_required
from ..modules import ProductCategory, Products

order_bp = Blueprint("order", __name__)

@order_bp.route('/getProductListInfo', methods=['GET'])
@jwt_required
def tea_list():
    productLists = ProductCategory.query.all()
    return json.jsonify(
        status="success",
        data=[i.serialize for i in productLists]
    )

@order_bp.route('/getProductInfo', methods=['GET', 'POST'])
def tes_info():
    req_data = json.loads(request.data)
    id = req_data.get("id")
    
    pass