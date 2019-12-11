from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from wtforms import ValidationError

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager


@login_manager.user_loader
def load_user(UserInfo_id):
    return UserInfo.query.get(int(UserInfo_id))


# 用户信息表
class UserInfo(UserMixin, db.Model):
    __tablename__ = "UserInfos"
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(64), nullable=True, unique=True, index=True)
    Email = db.Column(db.String(64), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(64), nullable=True)
    Sex = db.Column(db.String(5), nullable=True)
    confirmed = db.Column(db.Boolean, default=False)

    def __str__(self):
        return self.Username

    # 禁止读取密码
    @property
    def password(self):
        return self.password_hash

    # 写密码
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 验证密码
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 发送邮件时将用户名的id进行加密
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    # 点击视图是判断加密的字符串是否是用户的id
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data= s.loads(token)
        except:
            return None
        return UserInfo.query.get(data["id"])


# 文章表
class posts(db.Model):
    __tablename__ = 'Postss'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    body_html = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    updated = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow())
    author_id = db.Column(db.Integer, db.ForeignKey('UserInfos.id'), nullable=True)

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'author_url': url_for('api.get_user', id=self.author_id),
            'comments_url': url_for('api.get_post_comments', id=self.id),
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get("body")
        if body is None or body == "":
            raise ValidationError('文章没有正文')
        return posts(body=body)
