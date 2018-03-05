########################################
# create by :ding-PC
# create time :2018-03-02 10:52:08.198630
########################################
#!/usr/bin/env python

from gencode.gen_code import GenCode,GenProject_Flask

if __name__ == '__main__':
    rootpath = r'.'
    umlfile = r'./docs/test.mdj'
    g = GenCode(umlfile,rootpath)
    #  把boclass 汇出成 swagger class
    g.export(umlfile,umlfile)
    #  产生model单元，type= flask:产生flask_sqlalchemy 的 model
    #               type = sql ：产生 sqlalchemy 的 model
    g.model()
    p = GenProject_Flask(umlfile, rootpath)
    # 产生专案代码
    p.gen_code()
