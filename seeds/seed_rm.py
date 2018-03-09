########################################
# create by :ding-PC
# create time :2018-03-08 12:02:25.983533
########################################
'''
初始化权限资料
'''
from seeds.models_rm import *
from app.models import *
from app import create_app_swagger
def init_rm_data(config):
    app = create_app_swagger(config).app
    app_context = app.app_context()
    app_context.push()
    current_app.logger.info('start add right seeds ')
    db.create_all()
    # todo add right data
    # sample code
    # # 人事系统
    # empsys = add_sys1('emp0','empsys')
    # # 员工管理
    # employeemng = add_sys2(empsys,'employeemng','员工管理')
    # #   员工资料和浏览(1),新增(2),修改(3),删除(4)操作
    # employee = add_sys3_and_op(empsys,employeemng,'employee','员工资料')
    # 增加第5个操作
    # add_sys3_op(employee, 'aud', '审核',5)
    # employee_pic = add_sys3(empsys,employeemng,'employee_pic','员工图片')
    # add_sys3_op(employee_pic, 'view', '浏览图片', 1)
    # add_sys3_op(employee_pic, 'insert', '上传图片',2)
    # add_sys3_op(employee_pic, 'delete', '删除图片', 4)
    current_app.logger.info('add right seeds success!')
