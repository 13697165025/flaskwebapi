
from flask import jsonify
from wtforms import ValidationError

from . import api

# 403请求中发送的身份验证凭据无权访问目标
def forbidden(message):
    response = jsonify({"error" : "forbidden", "message": message})
    response.status_code = 403
    return response


# 401请求未包含身份验证信息，或者提供的凭据无效
def unauthorized(message):
    response = jsonify({"error": "Unauthorized", "message": message})
    response.status_code = 401
    return response


# 400请求无效或不一致
def bad_request(message):
    response = jsonify({"error": "BadRequest", "message": message})
    response.status_code = 400
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])

