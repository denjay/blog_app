########################################
# create by :ding-PC
# create time :2018-03-02 10:52:55.895595
########################################
from flask import Flask
from flask_migrate import Migrate
from app.models import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data-dev.sqlite'
db.init_app(app)
migrate = Migrate(app, db)
