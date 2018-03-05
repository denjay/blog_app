########################################
# create by :ding-PC
# create time :2018-03-02 15:10:33.234703
########################################
from app import db
from datetime import datetime, timedelta
import json
from enum import Enum


class User_base(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True)
    user_password = db.Column(db.String(50))
    user_email = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                if hasattr(self, key)
                }


class Article_base(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(50), nullable=False)
    article_content = db.Column(db.String(50), nullable=False)
    article_date = db.Column(db.DateTime)
    click = db.Column(db.Integer)
    userid = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    user = db.relationship("User", foreign_keys="Article.userid")

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                if hasattr(self, key)
                }


class Comment_base(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(50))
    comment_date = db.Column(db.DateTime)
    userid = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    articleid = db.Column(db.Integer, db.ForeignKey("article.article_id"), nullable=False)
    user = db.relationship("User", foreign_keys="Comment.userid")
    article = db.relationship("Article", foreign_keys="Comment.articleid")

    def __repr__(self):
        return json.dumps(self.to_json())

    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                if hasattr(self, key)
                }
