########################################
# create by :ding-PC
# create time :2018-03-02 15:10:33.832472
########################################
import connexion
from flask_redis import FlaskRedis
from config import config
from flask_cors import CORS
import logging

from flask_sqlalchemy import SQLAlchemy
from mwauth.kong_auth import KongAuth
from mwpermission.permission import Permission


rds = FlaskRedis(strict=False)

db = SQLAlchemy()
auth = KongAuth()
p = Permission()

def create_app_swagger(config_name):
    conf = config[config_name]
    app_swg = connexion.App(__name__,
                            port = conf.PORT,
                            debug= conf.DEBUG,
                            specification_dir='../swagger/'
                            )
    yaml_host=app_swg.add_api('./1_0/api.yaml', arguments={'title': 'api 1.0'})
    app = app_swg.app
    CORS(app)
    app.config.from_object(conf)
    config[config_name].init_app(app)
    # 如果服務不需要註冊到kong，需修改host的設定
    if app.config['KONG_AUTO_REGISTER']:
        from mwsdk import Kong
        kong = Kong()
        yaml_host.specification['host'] = '%s:%s'%(kong.ip,kong.port)
    else:
        from mwsdk import AgentConf
        yaml_host.specification['host'] = '%s:%s' % (AgentConf().bind_ip, app.config['PORT'])
    # 需要增加handler 这样docker 中才能看到log
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(formatter)
    app.logger.addHandler(consoleHandler)
    app.logger.level = app.config['LOG_LEVEL']
    rds.init_app(app)
    
    db.init_app(app)
    auth.init_app(app)
    p.init_app(app)
    
    return app_swg

