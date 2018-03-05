########################################
# create by :ding-PC
# create time :2018-03-02 15:10:33.818635
########################################
from app import auth, db, p
from app.models import *


@auth.valid_login
@p.check("user", ["view"])
def users_get(page=None, per_page=None) -> str:
    datap = User.query.order_by(User.id).paginate(page, per_page)
    return [data.to_json() for data in datap.items], \
           200, {"content-type": "chatset=utf8", "x-page": datap.page, "x-total": datap.total}


@auth.valid_login
@p.check("user", ["insert"])
def users_post(body) -> str:
    try:
        data = User(**body)
        db.session.add(data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return data.to_json(), 201, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("user", ["view"])
def users_id_get(id) -> str:
    data = User.query.filter_by(id=id).first_or_404()
    return data.to_json(), 200, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("user", ["edit"])
def users_id_put(id, body) -> str:
    try:
        User.query.filter(User.id == id).update(body)
    except Exception as e:
        db.session.rollback()
        return {"error", str(e)}, 422, {"content-type": "chatset=utf8"}
    data = User.query.filter_by(id=id).first_or_404()
    return data.to_json(), 201, {"content-type": "chatset=utf8"}


@auth.valid_login
@p.check("user", ["delete"])
def users_id_delete(id) -> str:
    try:
        db.session.query(User).filter(User.id == id).delete()
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
    return "", 204
