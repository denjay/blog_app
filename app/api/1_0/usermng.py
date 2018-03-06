########################################
# create by :ding-PC
# create time :2018-03-06 14:48:36.801695
########################################
from app import db, p
from app.auths import Auth
from app.models import *
# @auth.valid_login
# @p.check("user", ["view"])
@Auth.login_required
def users_id_get(id) -> str:
    data = User.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
# @auth.valid_login
# @p.check("user", ["edit"])
@Auth.login_required
def users_id_put(id,body) -> str:
    try:
        User.query.filter(User.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = User.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
# @auth.valid_login
# @p.check
@Auth.login_required
def users_id_delete(id) -> str:
    try:
        db.session.query(User).filter(User.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
# @auth.valid_login
# @p.check("user", ["insert"])
def users_login_post(body) -> str:
    username = body['user_name']
    password = body['user_password']
    user = User.query.filter_by(user_name=username).first_or_404()
    if user.user_password == password:
        token = Auth.encode_auth_token(user.id)
        return {'result': '登录成功'}, 200, {"Access-Control-Expose-Headers": 'Authorization',
                                         "Authorization": "Bearer " + str(token)}
# @auth.valid_login
# @p.check("user", ["insert"])
def users_register_post(body) -> str:
    try:
        data = User(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return {"message": "注册成功"}, 201, {"content-type": "chatset=utf8"}
