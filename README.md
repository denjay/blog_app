########################################
# 用starUML工具生成博客后端代码
# create by :ding-PC
# create time :2018-03-02 10:52:55.871206
########################################

### install package
```
pip install -r requirements.txt
```
### run
python run.py

### swagger debug:
```
http://localhost:8888/test/v1.0/ui/

```

### 环境变量设定
```
True：自動註冊到kong
auto_register2kong = os.environ.get('kong_auto_register') or  conf_parse.getboolean('reg_service','kong',fallback=False)
True:自動註冊到consul
auto_register2consul = os.environ.get('consul_auto_register') or  conf_parse.getboolean('reg_service','consul',fallback=False)
web_port =os.environ.get('web_port') or conf_parse.getint('web','port',fallback=8000)
```

### 执行docker
  sudo ./run.sh


### 数据迁移
> 支持对开发环境下的sqlite资料的数据迁移，不建议在生产环境中执行，避免人工失误，导致损坏资料
1. install or upgrade
```bash
pip install --upgrade Flask-Migrate
```
2.指定Flask app
> linux 下
```bash
export FLASK_APP=migrate_run.py
```
> windows 下
```bash
set FLASK_APP=migrate_run.py
```
3. 初始化
```bash
flask db init
```
4. 产生迁移语句
```bash
flask db migrate
```
5. 执行升级资料库
```bash
flask db upgrade
