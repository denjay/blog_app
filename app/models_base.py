########################################
# create by :ding-PC
# create time :2018-03-08 12:02:25.181877
########################################
from app import db
from datetime import datetime,timedelta
import json
from enum import Enum
class User_base(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique= True)
    user_password = db.Column(db.String(50))
    user_email = db.Column(db.String(50), unique= True)
    articles = db.relationship("Article", back_populates="user", foreign_keys="Article.userid", cascade="all, delete-orphan")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Article_base(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    article_title = db.Column(db.String(50), nullable= False)
    article_content = db.Column(db.String(50), nullable= False)
    article_date = db.Column(db.DateTime, default= datetime.now)
    click = db.Column(db.Integer, default= 0)
    userid = db.Column(db.Integer,db.ForeignKey("user.id"), nullable= False)
    user = db.relationship("User", back_populates="articles", foreign_keys="Article.userid")
    comments = db.relationship("Comment", back_populates="article", foreign_keys="Comment.articleid", cascade="all, delete-orphan")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
class Comment_base(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment_content = db.Column(db.String(50))
    comment_date = db.Column(db.DateTime, default= datetime.now)
    userid = db.Column(db.Integer,db.ForeignKey("user.id"), nullable= False)
    articleid = db.Column(db.Integer,db.ForeignKey("article.id"), nullable= False)
    user = db.relationship("User", foreign_keys="Comment.userid")
    article = db.relationship("Article", back_populates="comments", foreign_keys="Comment.articleid")
    def __repr__(self):
        return json.dumps(self.to_json())
    def to_json(self):
        return {key: getattr(self, key) for key in self.__table__.columns.keys()
                   if hasattr(self,key)
               }
