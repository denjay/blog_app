########################################
# create by :ding-PC
# create time :2018-03-02 10:52:55.896162
########################################
#!/usr/bin/env bash
set FLASK_APP=migrate_run.py
flask db init
flask db migrate
flask db upgrade
