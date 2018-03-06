########################################
# create by :ding-PC
# create time :2018-03-06 14:48:36.838254
########################################
from app import auth, db, p
from app.models import *
@auth.valid_login
@p.check("comment", ["view"])
def comments_get(page = None,per_page = None) -> str:
    datap = Comment.query.order_by(Comment.id).paginate(page, per_page)
    return [data.to_json() for data in datap.items], \
           200, {"content-type": "chatset=utf8", "x-page": datap.page, "x-total": datap.total}
@auth.valid_login
@p.check("comment", ["insert"])
def comments_post(body) -> str:
    try:
        data = Comment(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("comment", ["view"])
def comments_id_get(id) -> str:
    data = Comment.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("comment", ["edit"])
def comments_id_put(id,body) -> str:
    try:
        Comment.query.filter(Comment.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = Comment.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}
@auth.valid_login
@p.check("comment", ["delete"])
def comments_id_delete(id) -> str:
    try:
        db.session.query(Comment).filter(Comment.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
