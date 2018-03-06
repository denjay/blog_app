import jwt
import datetime
from flask import request
import config


# from .. import common


class Auth(object):
    @staticmethod
    def encode_auth_token(user_id):
        """
        生成认证Token
        :param user_id: int
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ding',
                'data': {
                    'id': user_id
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(eval(auth_token), config.SECRET_KEY, options={'verify_exp': False})
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @staticmethod
    def login_required(func):
        def wrapper(*args, **kw):
            auth_token = request.headers.get("Authorization")
            if auth_token:
                return func(*args, **kw)
            else:
                return {'messagge': '请登录'}
        return wrapper
