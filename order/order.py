from flask import Blueprint, json, request

from ..auth.myJwt import jwt_required, current_user
from ..modules import db, ProductCategory, Order, UserInfo, Products

order_bp = Blueprint("order", __name__)

@order_bp.route('/getProductListInfo', methods=['GET'])
@jwt_required
def tea_list():
    print('current_user')
    print(current_user)
    productLists = ProductCategory.query.all()
    return json.jsonify(
        status="success",
        data=[i.serialize for i in productLists]
    )

@order_bp.route('/getProductInfo', methods=['GET'])
@jwt_required
def tes_info():
    req_data = json.loads(request.data)
    id = req_data.get("id")
    pass


@order_bp.route('/order', methods=['POST'])
@jwt_required
def order():
    """
    处理点单数据：[{ product_id, product_num }]
    """
    req_data = json.loads(request.data)
    try:
        price = 0
        user = UserInfo.query.filter_by(username=current_user).first()
        if user is None: 
            return json.jsonify(status='error', msg='invalid username')
        for data in req_data:
            order = Order(user.uid, data.product_id, data.product_num)
            price += Products.query.filter_by(id=data.product_id).first().price
            db.session.add(order)
        if (user.wallet < price):
            return json.jsonify(status='error', msg='Insufficient Balance') # 余额不足
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return json.jsonify(status='success')