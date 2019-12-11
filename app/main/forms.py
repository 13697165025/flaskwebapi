from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError
from app.models import UserInfo
from flask import session


# 登录表单
class LoginForm(FlaskForm):
    Email = StringField(label="邮箱", validators=[DataRequired('不能为空'), Email('邮箱不合法')])
    pwd = PasswordField(label="密码", validators=[DataRequired('不能为空')])
    remember_me = BooleanField(label="保持密码")
    submit = SubmitField(label="提交")


# 注册表单
class RegisterForm(FlaskForm):
    user = StringField(label="用户名", validators=[DataRequired(), Length(min=4, max=9, message="用户名的长度在4-9之间")])
    Email = StringField(label="邮箱", validators=[DataRequired('不能为空'), Email('邮箱不合法')])
    pwa1 = PasswordField(label="密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间")])
    pwa2 = PasswordField(label="新密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间"), EqualTo(fieldname='pwa1', message="两次密码不一致！")])
    sex = RadioField(label="性别", choices=[('1', '男'), ('2', '女')])
    age = IntegerField(label="年龄", validators=[DataRequired()])
    submit = SubmitField(label="提交")

    def validate_Email(self, field):
        # if UserInfo.query.filter_by(email= field.)
        pass


# 类别表单
class TypeForm(FlaskForm):
    typename = StringField(label="类别名称", validators=[DataRequired()])
    submit = SubmitField(label="提交")


# 修改密码表单
class PasswordChangeForm(FlaskForm):
    oldpassword = PasswordField(label="旧密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间") ])
    newpassword = PasswordField(label="新密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间")])
    password = PasswordField(label="确认密码", validators=[DataRequired(),Length(min=6, max=12, message="密码必须要在6-12之间"), EqualTo(fieldname='newpassword', message="两次密码不一致！") ])
    submit = SubmitField(label="提交")

    def validate_newpassword(self, field):
        User1 = UserInfo.query.filter_by(id=session['id']).first()
        if User1.verify_password(field.data):
            raise ValidationError('新密码不能和旧密码一致！！')


# 邮箱更新表单
class EmailChangeForm(FlaskForm):
    Email = StringField(label="邮箱", validators=[DataRequired('不能为空'), Email('邮箱不合法')])
    password = PasswordField(label="密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间") ])
    submit = SubmitField(label="提交")


# 重置密码表单
class ResetPasswordForm(FlaskForm):
    Email = StringField(label="邮箱", validators=[DataRequired('不能为空'), Email('邮箱不合法')])
    submit = SubmitField(label="提交")

    def validate_Email(self, field):
        User1 = UserInfo.query.filter_by(id=session['id']).first()
        if User1.Email != field.data:
            raise ValidationError('邮箱不存在！')


# 重置密码表单2
class ResetPassForm(FlaskForm):
    newpassword = PasswordField(label="新密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间")])
    password = PasswordField(label="确认密码", validators=[DataRequired(), Length(min=6, max=12, message="密码必须要在6-12之间"), EqualTo(fieldname='newpassword', message="两次密码不一致！")])
    submit = SubmitField(label="提交")


