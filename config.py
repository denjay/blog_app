########################################
# create by :ding-PC
# create time :2018-03-02 10:52:55.891907
########################################
import os
from mwutils.utils import getConfig
from mwutils.mw_consul import DatabaseConf,RedisConfMaster

basedir = os.path.abspath(os.path.dirname(__file__))
conf_parse  = getConfig(__file__)
SECRET_KEY = "dingxianjie"

#################################################################
# 在config.ini中app_config.config=development 时为开发者模式，
# 开发者模式使用DevelopmentConfig，所有配置在DevelopmentConfig中手动设定
# 开发者模式只需要开启dev 模式的consul(命令：consul agent dev)即可
# 不需要kong认证，认证信息在DevelopmentConfig设定
# 注意：开发者模式不允许在生产环境中使用，否则会引起安全性问题
###################################################################
is_development = conf_parse.get('app_config','config', fallback='production')=='development'

class Config:
    URL_PREFIX_SCH = ''
    DEBUG = False
    TESTING = False
    PORT = 8080
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess maxwin password'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    
    @staticmethod
    def init_app(app):
        pass
class TestingConfig(Config):
    PORT = 9999
    DEBUG = True
    TESTING = True
    LOG_LEVEL = 10
    # True 开发模式，会跳过权限检查
    DEVELOPMENT = True
    # True自动注册到kong，False不做
    KONG_AUTO_REGISTER = False
    # True自动注册到consul，False不做
    CONSUL_AUTO_REGISTER = False
    REDIS_URL = 'redis://192.168.101.33:6380/0'
    
    # 开发模式下的登录用户
    LOGIN_USER_NAME = 'super'
    # 开发模式下的用户ID
    LOGIN_USER_ID = '1999'
    SYSTEM_NAME = 'test'
    # 输出sql
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class DevelopmentConfig(Config):
    DEBUG = True
    PORT = 8800
    # 输出log为debug
    LOG_LEVEL = 10
    # True 开发模式，会跳过权限检查
    DEVELOPMENT = True
    # True自动注册到kong，False不做
    KONG_AUTO_REGISTER = False
    # True自动注册到consul，False不做
    CONSUL_AUTO_REGISTER = False
    
    # 开发模式下的登录用户
    LOGIN_USER_NAME = 'super'
    # 开发模式下的用户ID
    LOGIN_USER_ID = '1999'
    # LOGIN_USER_SYSTEMUSER=True
    # LOGIN_USER_MANAGEUSER=False
    # LOGIN_USER_MANAGEUSER_ID=''
    SYSTEM_NAME = 'kaoqing'
    # 输出sql
    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    # SQLALCHEMY_DATABASE_URI = "mssql+pymssql://sa:111@192.168.101.238:1433/gxtest"
    # SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root:111@192.168.101.33:3306/ms"
    
    REDIS_URL ='redis://192.168.101.33:6380/0'
class ProductionConfig(Config):
    PORT = int(os.environ.get('WEB_PORT') or conf_parse.getint('web','port',fallback=8001))
    
    # 权限用的系统名
    SYSTEM_NAME =  os.environ.get('SYSTEM_NAME','kaoqing')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = DatabaseConf(os.environ.get('DATABASE_NAME','kaoqing')).\
                              sqlalchemy_database_uri() if not is_development else ''
    
    REDIS_URL =RedisConfMaster().redis_url() if not is_development else ''
    LOG_LEVEL = int(os.environ.get('LOG_LEVEL',conf_parse.getint('log', 'level', fallback= 20)))
    # True自动注册到kong，False不做
    KONG_AUTO_REGISTER = os.environ.get('KONG_AUTO_REGISTER',str(conf_parse.getboolean('reg_service','kong',fallback=False))).lower()=='true'
    # True自动注册到consul，False不做
    CONSUL_AUTO_REGISTER = os.environ.get('CONSUL_AUTO_REGISTER',str(conf_parse.getboolean('reg_service','consul',fallback=False))).lower()=='true'
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig if not is_development else DevelopmentConfig
}
if __name__ == '__main__':
    conf = config['default']
    print(conf.PORT)
    print(config['default'].PORT)
