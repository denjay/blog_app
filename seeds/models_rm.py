########################################
# create by :ding-PC
# create time :2018-03-08 12:02:25.982394
########################################
'''
权限模块
'''
from datetime import datetime
from app import db
from flask import current_app
from .seed_utils import add_seed
def add_sys1(sys1id,sys1_name,sys1_caption=None):
    '''
    增加根权限系统
    :param sys1id: 第一层权限的id
    :param sys1_name:第一层权限的名称
    :param sys1_caption: 第一层权限的描述
    :return:第一层权限的 subsystem物件
    '''
    # 大部分情况下不需要caption，避免覆盖其他地方的修改
    if sys1_caption is None:
        sys1 = add_seed(db.session,
                    Subsystem,
                    {'id':sys1id},
                    {'id':sys1id,'name':sys1_name,'parentid':'000'})
    else:
        sys1 = add_seed(db.session,
                        Subsystem,
                        {'id': sys1id},
                        {'id': sys1id, 'name': sys1_name,'caption':sys1_caption, 'parentid': '000'})
    return sys1
def add_sys2(sys1,sys2_name,sys2_caption):
    '''
    增加第二级权限
    :param sys1:第一层权限物件
    :param sys2_name: 第二层权限名
    :param sys2_caption:第二层权限描述
    :return:
    '''
    sys2 = add_seed(db.session,
                    Subsystem,
                    {'id':'%s-%s-2'%(sys1.id,sys2_name)},
                    {'id':'%s-%s-2'%(sys1.id,sys2_name),'name':sys2_name,'caption':sys2_caption,'parentid':sys1.id})
    return sys2
def add_sys3(sys1,sys2,sys3_name,sys3_caption):
    '''
    第三级权限
    :param sys1:权限系统
    :param sys2:权限的第二层节点
    :param sys3_name : 英文名
    :param sys3_caption : 中文名
    :param ops: 有些权限可能只有浏览
    :return:
    '''
    sys3 = add_seed(db.session,
                    Subsystem,
                    {'id':'%s-%s-3'%(sys1.id,sys3_name)},
                    {'id':'%s-%s-3'%(sys1.id,sys3_name),'name':sys3_name,'caption':sys3_caption,'parentid':sys2.id})
    return sys3
def add_sys3_op(sys3,op_name,op_caption,op):
    '''
    增加第三级权限下的操作,比如：op_name:upload,op_caption:上传文件，op:5
    :param sys3: boclass
    :param op_name: upload
    :param op_caption: 上传文件
    :param op: 操作码，比如：5
    :return:
    '''
    sys3_op=add_seed(db.session,
             Action,
             {'id': '%s-%s' % (sys3.id,op)},
             {'id': '%s-%s' % (sys3.id,op) , 'name': op_name, 'caption': op_caption, 'subsystemid': sys3.id,'operation':op})
    return sys3_op
def add_sys3_and_op(sys1,sys2,sys3_name,sys3_caption,ops=None):
    '''
    增加第三级boclass的权限和该boclass 下的1浏览，2新增，3修改，4删除。。。
    :param cls:权限类
    :param sys1:权限系统
    :param sys2:权限的第二层节点
    :param sys3_caption : 类别的中文名
    :param ops: 有些权限可能只有浏览，新增，如：[1,2]
    :return:
    '''
    if ops is None:
        ops = [1,2,3,4]
    cls_name = sys3_name.lower()
    sys3 = add_sys3(sys1,sys2,cls_name,sys3_caption)
    if 1 in ops:
        add_sys3_op(sys3,'view','浏览',1)
    elif 2 in ops:
        add_sys3_op(sys3,'insert','新增',2)
    elif 3 in ops:
        add_sys3_op(sys3,'edit','修改',3)
    elif 4 in ops:
        add_sys3_op(sys3,'delete','删除',4)
    return sys3
def new_id():
    sql_url=current_app.config['SQLALCHEMY_DATABASE_URI']
    newid='0'
    if sql_url.startswith('mysql+mysqldb'):
        connection = db.engine.raw_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("sp_getobjectids_new", [1])
            newid = cursor.fetchone()[0]
            cursor.close()
            connection.commit()
        finally:
            connection.close()
        # newid = db.session.execute('call sp_getobjectids_new(1,@a);select @a;').fetchone()[0]
    elif sql_url.startswith('mssql+pymssql'):
        newid = db.session.execute(' declare @RETURNVALUE int '
                                   ' exec [dbo].[sp_GetObjectIDs_new] 1, @RETURNVALUE output '
                                   ' select @RETURNVALUE').fetchone()[0]
    return str(newid)
class Role(db.Model):
    __tablename__ = 'approle'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(50))
    # 管理员新增的用户只能是False
    issystem = db.Column(db.Boolean,default=False)
    def to_json(self):
        return {"id":self.id,
                "name":self.name,
                "issystem":self.issystem or False,
                "description":self.description}
    def __repr__(self):
        return '<AppRole %r>' % self.name
class Subsystem(db.Model):
    __tablename__ = 'subsystem'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    caption = db.Column(db.String(50))
    parentid = db.Column(db.String(50), db.ForeignKey('subsystem.id'))
    subsystems = db.relationship("Subsystem")
    actions = db.relationship("Action")
    def __repr__(self):
        return "subsystem(name:%s,caption:%s)"%(self.name,self.caption)
class Action(db.Model):
    __tablename__ = 'appaction'
    id = db.Column(db.String(50),primary_key=True)
    name = db.Column(db.String(50))
    caption = db.Column(db.String(50))
    subsystemid = db.Column(db.String(50),db.ForeignKey('subsystem.id'))
    operation = db.Column(db.Integer,default=1)
    def __repr__(self):
        return "appaction(name:%s,operation:%d)"%(self.name,self.operation)
class Userrole(db.Model):
    __tablename__ = 'appuserrole'
    id = db.Column(db.String(50),primary_key=True)
    appuserid = db.Column(db.String(50))
    approleid = db.Column(db.String(50))
    def __repr__(self):
        return "appuserrole(appuserid:%s,approleid:%s)"%(self.appuserid,self.approleid)
class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.String(50),primary_key=True)
    ptype = db.Column(db.Integer)
    appactionid = db.Column(db.String(50))
    baseactorid = db.Column(db.String(50))
    def __repr__(self):
        return "permission(id:%s,actorid:%s,actionid:%s,pttype:%d)"%\
               (self.id,self.baseactorid,self.appactionid,self.ptype)
class User(db.Model):
    __tablename__ = 'appuser'
    uid = db.Column('id',db.String(50), primary_key=True)
    uname = db.Column("name",db.String(64), unique=True, index=True)
    passwordmd5 = db.Column("passwordmd5",db.String(100))
    description = db.Column(db.String(100))
    modifydatetime = db.Column(db.DateTime,default=datetime.now())
    insertdatetime = db.Column(db.DateTime, default=datetime.now())
    systemuser = db.Column('issystemuser',db.Boolean,default=False)
    manageuser = db.Column('ismanage',db.Boolean,default = False)
    manageuserid = db.Column(db.String(50),default = '')
    def to_json(self):
        return {"uid":self.uid,
                "uname":self.uname,
                "description":self.description,
                "systemuser":self.systemuser,
                'manageuser':self.manageuser,
                'manageuserid':self.manageuserid
                }
    def __repr__(self):
        return "user(id:%s),username:%s,issystemuser:%s"%(self.id,self.username,self.issystemuser)
