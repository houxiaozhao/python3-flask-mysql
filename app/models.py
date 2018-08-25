from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
        }


categorys = db.Table('categorys',
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                     )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    categorys = db.relationship('Category', secondary=categorys, backref=db.backref('posts', lazy='dynamic'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
