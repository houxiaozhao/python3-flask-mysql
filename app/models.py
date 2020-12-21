from datetime import datetime

from app import db
from app.baseModel import BaseModel


class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    # 如果您想要一对一关系，您可以把 uselist=False 传给 relationship() 。
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    _default_fields = [
        "username",
    ]
    _hidden_fields = []
    _readonly_fields = []

    def __repr__(self):
        return '<User {}>'.format(self.username)


categorys = db.Table('categorys',
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                     )


class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 添加外键声明
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categorys = db.relationship('Category', secondary=categorys, backref=db.backref('posts', lazy='dynamic'))
    _default_fields = [
        "body",
    ]
    _hidden_fields = []
    _readonly_fields = []

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
