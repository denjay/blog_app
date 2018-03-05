########################################
# create by :ding-PC
# create time :2018-03-02 10:52:55.886802
########################################
from app import create_app_swagger


# def create_dev_db():
#     from app import create_app_swagger, db
#     from app.models import Order, Request, Customer, Quote
#     app_sw = create_app_swagger('default')
#     app = app_sw.app
#     app_context = app.app_context()
#     app_context.push()
#     #db.d*r*o*p*_*all()
#     db.create_all()

def register_service(config_name, app):
    from config import config
    # 注册本服务到kong
    config = config[config_name]
    auto_register2consul = config.CONSUL_AUTO_REGISTER
    auto_register2kong = config.KONG_AUTO_REGISTER
    web_port = config.PORT
    from mwsdk import AgentConf
    service_host = '%s:%s' % (AgentConf().bind_ip, web_port)
    app.logger.info('auto_register2kong:%s' % auto_register2kong)
    if auto_register2kong:
        from mwsdk import Kong
        kong = Kong()
        kong.reg_service('test/v1.0', service_host, auth='jwt')
        app.logger.info('注册kong成功')
        # kong.reg_service('xxxx/v1.0/login_jwt', service_host, auth='')
        # kong.reg_service('xxxx/v1.0/logout_jwt', service_host,auth='jwt')
        # kong.reg_service('static', service_host, auth='', kong_uris='/auth/static')
    # 註冊到kong的服務到consul
    app.logger.info('auto_register2consul:%s' % auto_register2consul)
    if auto_register2consul:
        check = {"id": "test api",
                 "name": "test on port %s" % web_port,
                 "http": "http://%s/test/v1.0/health" % service_host,
                 "interval": "20s",
                 "timeout": "10s",
                 "DeregisterCriticalServiceAfter": "5m"
                 }
        from mwsdk import Kong, reg_service
        kong = Kong()
        reg_service('test', address=kong.ip, port=kong.port, tags=['kong', 'jwt'],
                    check=check)
        app.logger.info('注册consul成功')


if __name__ == '__main__':
    # create_dev_db()
    app = create_app_swagger('default')
    register_service('default', app.app)
    app.run(host='0.0.0.0')
    if app.config.get('CONSUL_AUTO_REGISTER'):
        from mwsdk import Kong, dereg_service

        dereg_service('test', Kong().port)
