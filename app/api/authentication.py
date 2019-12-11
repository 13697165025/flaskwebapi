
# API用户认证
from app.models import *
from .errors import unauthorized, forbidden
from . import api
from flask import g, jsonify, request, json
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


# 验证请求(根据请求所带认证信息)是否是认证请求，、
@auth.verify_password
def verify_password(email_or_token, password):
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = UserInfo.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = UserInfo.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized("用户身份为认证")


# 若想保护路由, 可使用auth.login_required 装饰器
@api.route('/posts/')
@auth.login_required
def get_posts():
    pass


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and not g.current_user.confirmed:
        return forbidden("未认证或激活的账号！")


@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('无效的用户')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})


@api.route('/posts/', methods=['POST'])
def new_post():
    post = posts.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_json())

# json.dumps({"k": 12}) 将字典转为json  json.loads({"k":12}) 将json转为字典


@api.route('/posts/')
def get_postss():
    postss = posts.query.all()
    return jsonify({'posts': [post.to_json() for post in postss] })


@api.route('/posts/<int:id>')
def get_post(id):
    post = posts.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route("/user/<int:id>/")
def userid(id):
    user = UserInfo.query.filter_by(id=id).first()
    list = []
    list.append(user.__dict__)
    return jsonify(list)




