import time
from functools import wraps
from werkzeug.local import LocalProxy
from flask.json import jsonify
import jwt
from flask.globals import request
from flask import current_app, _request_ctx_stack

current_user = LocalProxy(lambda: getattr(_request_ctx_stack.top, 'current_user', None))

def generate_jwt(payload: dict, secret=None):
    """
    生成jwt，返回token
    """
    expiry = round(time.time() * 1000) + current_app.config['JWT_EXPIRATION_DELTA']
    
    payload.update({'exp': expiry})
    if not secret:
        secret = current_app.config['JWT_SECRET']
    token = jwt.encode(payload, secret, algorithm='HS256')
    return token

def verify_jwt(token, secret=None):
    """
    检验jwt，返回decode的结果。若检验失败返回None
    """
    if not secret:
        secret = current_app.config['JWT_SECRET']
    
    try:
        payload = jwt.decode(token, secret, algorithms='HS256')
    except jwt.PyJWTError:
        return None
    
    expiry = payload.get('exp')
    if expiry is None or expiry <= round(time.time() * 1000):
        return None
    
    return payload

def jwt_required(fn):
    @wraps(fn)
    def wapper(*args, **kwargs):
        auth_jwt = request.headers.get('Authorization')
        if not auth_jwt:
            return jsonify({'status': 'error', 'msg': '认证错误'})
        
        parts = auth_jwt.split()
        if len(parts) != 2:
            return jsonify(status='error', msg='Token无效')

        token = parts[1]
        payload = verify_jwt(token)
        if payload is None:
            return jsonify(status='error', msg='Token无效')
        
        if payload.get('username') is None:
            return jsonify(status='error', msg='Token无效')

        _request_ctx_stack.top.current_user = payload.get('username')
        return fn(*args, **kwargs)
    return wapper