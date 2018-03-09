########################################
# create by :ding-PC
# create time :2018-03-08 12:02:25.968843
########################################
from copy import deepcopy
from flask import request, jsonify
from app.auths import Auth
from app import auth, db, p
from app.models import *


@auth.valid_login
@p.check("article", ["view"])
def articles_get(page=None, per_page=None) -> str:
    articles = Article.query.order_by(Article.id)
    count = articles.count()
    datap = articles.paginate(page, per_page)
    print({"articles": [data.to_json() for data in datap.items], "count": count})
    return jsonify({"articles": [data.to_json() for data in datap.items], "count": count}), 200, {
        "content-type": "chatset=utf8", "x-page": datap.page, "x-total": datap.total}


@Auth.login_required
def articles_post(body) -> str:
    try:
        data = Article(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("article", ["view"])
def articles_hot_get() -> str:
    datas = Article.query.all()
    return [data.to_json() for data in datas], 200, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("article", ["view"])
def articles_id_get(id) -> str:
    data = Article.query.filter_by(id=id).first_or_404()
    data_copy = deepcopy(data)
    data_json = data.to_json()
    data_json['click'] += 1
    return data_copy.to_json(), 200, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("article", ["edit"])
def articles_id_put(id, body) -> str:
    try:
        Article.query.filter(Article.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Article.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("article", ["delete"])
def articles_id_delete(id) -> str:
    try:
        db.session.query(Article).filter(Article.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204


@auth.valid_login
@p.check("comment", ["view"])
def articles_id_comments_get(id) -> str:
    article = Article.query.filter_by(id=id).first_or_404()
    comments = article.comments
    comments_json = []
    for comment in comments:
        comment_json = comment.to_json()
        comment_json.update({"user_name": comment.user.user_name})
        comments_json.append(comment_json)
    return comments_json


def articles_id_comments_post(body, id) -> str:
    auth_token = request.headers.get("Authorization")[7:]
    payload = Auth.decode_auth_token(auth_token)
    if payload is False:
        return {'message': '无效令牌'}, 401
    user_id = payload["data"]['id']
    data = eval(request.data)
    data.update({'userid': user_id, 'articleid': id,
                 'comment_date': datetime.utcnow()})
    try:
        comment = Comment(**data)
        db.session.add(comment)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
        return {'message': '评论提交失败'}, 400
    return data
