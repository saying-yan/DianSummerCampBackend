from flask import json, jsonify, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required

from ..modules import db, UserInfo
from .myJwt import generate_jwt, jwt_required, current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    登录接口
    """
    # if current_user.is_authenticated:
    #     return jsonify({'status': 'error', 'msg': '已登录'})
    # admin = UserInfo.query.filter_by(username='admin').first()
    print(current_user)
    req_data = json.loads(request.data)

    username = req_data.get('username')
    password = req_data.get('password')
    if username is None or password is None:
        return jsonify({'status': 'error', 'msg': '登录失败'})
    user = UserInfo.query.filter_by(username=username).first()
    if user is None or not user.validate_password(password):
        return jsonify({'status': 'error', 'msg': '登录失败'})
    
    payload = {'username': username}
    return jsonify(status='success', msg='', jwt=generate_jwt(payload))


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    注册接口
    """
    req_data = json.loads(request.data)

    username = req_data.get('username')
    phone_number = req_data.get('phone')
    password = req_data.get('password')
    if username is None or phone_number is None or password is None:
        return jsonify({'status': 'error', 'msg': '数据不能为空'})
    if (len(username.encode('utf-8')) < 3 or
        len(username.encode('utf-8')) > 10 or
        len(password.encode('utf-8')) < 6 or
        len(password.encode('utf-8')) > 18 or
        len(phone_number.encode('utf-8')) != 11 ):
        return jsonify({'status': 'error', 'msg': '数据长度错误'})

    if (UserInfo.query.filter_by(username=username).first()):
        return jsonify({'status': 'error', 'msg': '用户名已存在'})

    try:
        user = UserInfo(username, phone_number, password)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e
    return jsonify({'status': 'success', 'msg': ''})

@auth_bp.route('/test', methods=['GET', 'POST'])
# @jwt_required
def test():
    from ..utils.utils import init_mysql
    init_mysql()
    return jsonify({'status': 'success', 'msg': ''})
