########################################
# create by :ding-PC
# create time :2018-03-02 15:10:33.812983
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
