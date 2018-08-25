# python3 flask 使用Mysql数据库

1. 创建flask基本项目结构

    ```python
    from flask import Flask
    app = Flask(__name__)
    ```

2. 安装`flask-sqlalchemy`
    ```commandline
    pip install flask-sqlalchemy
    ```

3. 导入配置
    ```python
    from flask_sqlalchemy import SQLAlchemy
     
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/hhh'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db = SQLAlchemy(app)
    ```
    python3 不再支持MySQKdb,连接mysql数据库需要使用pymysql

    安装pymysql

    `pip install pymysql`

4. 定义表模型
    ```python
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=True)
    
        def __init__(self, username):
            self.username = username
    
        def __repr__(self):
            return '<User {}>'.format(self.username)
    ```

5. 创建表
   在python shell中

   ```commandline
    >>> from app import db
    >>> db.create_all()
   ```

6. 添加数据
   在python shell中
   ```commandline
    >>> from app import db
    >>> from app import User
    >>> user=User('hou')
    >>> db.session.add(user)
    >>> db.session.commit()
   ```

7. 查询数据库

   ```bash
    >>> User.query.all()
    [<User hou>]
    >>> User.query.filter_by(username='hou').first()
    <User hou>
   ```

8. 一对多或一对一表关联

   - 定义Post 表模型

     ```python
     from datetime import datetime
     class Post(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         body = db.Column(db.Text)
         timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
         # 添加外键声明
         user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
         def __repr__(self):
             return '<Post {}>'.format(self.body)
     ```

   - User添加关系

     ```python
     class User(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         username = db.Column(db.String(64), unique=True, nullable=True)
         # 新加的
         # 如果您想要一对一关系，您可以把 uselist=False 传给 relationship() 。
         posts = db.relationship('Post', backref='user', lazy='dynamic')
         def __init__(self, username):
             self.username = username
         def __repr__(self):
             return '<User {}>'.format(self.username)
     ```

   - 执行创建表

   - 添加数据

     ```bash
     >>> from app import *
     >>> user=User.query.filter_by(username='hou').first()
     >>> post1=Post(body='post1post1post1post1post1post1',user=user)
     >>> db.session.add(post1)
     >>> db.session.commit()
     ```

   - 查询数据

     ```bash
     >>> user=User.query.filter_by(username='hou').first()
     >>> user.posts.all()
     [<Post 哈哈哈哈哈>, <Post post1post1post1post1post1post1>]
     >>> user.posts.filter_by(id=4).first()
     <Post post1post1post1post1post1post1>
     ```

9. 多对多表关联

   - 定义Category 表模型

     ```python
     class Category(db.Model):
         id = db.Column(db.Integer, primary_key=True)
         name = db.Column(db.String(50))
         def __init__(self, name):
             self.name = name
         def __repr__(self):
             return '<Category %r>' % self.name
     ```

   - 定义关联表

     ```python
     categorys = db.Table('categorys',
                          db.Column('id', db.Integer, primary_key=True),
                          db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                          db.Column('category_id', db.Integer, db.ForeignKey('category.id'))
                          )
     ```

   - Post 中添加关系

     ```python
      categorys = db.relationship('Category', secondary=categorys, backref=db.backref('posts', lazy='dynamic'))
     ```

   - 执行创建表

   - 准备类别数据

     ```bash
     >>> from app import *
     >>> category1=Category(name="前端")
     >>> category2=Category(name="nodejs")
     >>> category3=Category(name="python")
     >>> db.session.add(category1)
     >>> db.session.add(category2)
     >>> db.session.add(category3)
     >>> db.session.commit()
     ```

   - 添加post

     ```bash
     >>> from app import *
     >>> category1=Category.query.get(1)
     >>> category2=Category.query.get(2)
     >>> category3=Category.query.get(3)
     >>> user=User.query.get(1)
     >>> post1=Post(body='关联的post',user=user,categorys=[category1])
     >>> post2=Post(body='关联的post',user=user,categorys=[category1,category2,category3])
     >>> db.session.add(post1)
     >>> db.session.add(post2)
     >>> db.session.commit()
     ```
