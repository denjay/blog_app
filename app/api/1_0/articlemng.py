########################################
# create by :ding-PC
# create time :2018-03-02 15:10:33.823598
########################################
from app import auth, db, p
from app.models import *
@auth.valid_login
@p.check("article",["view"])
def articles_get(page = None,per_page = None) -> str:
    datap = Article.query.order_by(Article.id).paginate(page,per_page)
    return [data.to_json() for data in datap.items] ,\
            200 ,{"content-type": "chatset=utf8","x-page":datap.page,"x-total":datap.total}
@auth.valid_login
@p.check("article",["insert"])
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
@p.check("article",["view"])
def articles_id_get(id) -> str:
    data = Article.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("article",["edit"])
def articles_id_put(id,body) -> str:
    try:
        Article.query.filter(Article.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Article.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("article",["delete"])
def articles_id_delete(id) -> str:
    try:
        db.session.query(Article).filter(Article.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
