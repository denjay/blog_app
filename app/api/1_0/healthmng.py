########################################
# create by :ding-PC
# create time :2018-03-06 14:48:36.779501
########################################
from app import auth, db, p
from app.models import *
def health_get() -> str:
    try:
        data = {}
        return data, 200, {"content-type": "chatset=utf8"}
    except Exception as e:
        # todo handle error
        return {"error": str(e)}, 422, {"content-type": "chatset=utf8"}
