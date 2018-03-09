########################################
# create by :ding-PC
# create time :2018-03-08 12:02:25.983264
########################################
'''
系统默认资料的初始化
'''
from app import create_app_swagger
from app.models import *
from seeds.seed_utils import add_seed
def init_default_data(config):
    app = create_app_swagger(config).app
    app_context = app.app_context()
    app_context.push()
    app.logger.info('start add default seeds ')
    db.create_all()
    # todo add default data
    # sample code
    # employee = add_seed(db.session,Employee,{'name':'李三'},{'name':'李三'})
    app.logger.info('add default seeds success')
