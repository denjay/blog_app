########################################
# create by :ding-PC
# create time :2018-03-08 12:02:25.982992
########################################
'''
开发用的测试数据
'''
from app import create_app_swagger,db
from app.models import *
from seeds.seed_utils import add_seed
def init_dev_data():
    app = create_app_swagger('development').app
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    # todo add dev data
    # sample code
    # company1 = add_seed(db.session,Company,{'company_name':'铨鼎科技测试'},{'company_name':'铨鼎科技测试'})
    # company_auth = add_seed(db.session,Company_auth,{'appuserid':'1999','companyid':company1.id},{'appuserid':'1999','companyid':company1.id})
    # depart1 = add_seed(db.session,Depart,{'companyid':company1.id},{'companyid':company1.id})
    # employee = add_seed(db.session,Employee,{'emp_name':'cxh'},{'emp_name':'cxh','departid':depart1.id})
