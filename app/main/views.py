from flask import render_template, session, redirect, url_for, request, jsonify, flash, current_app
from app.models import *
from app.main.forms import *
from . import main
from flask_login import login_user, logout_user, login_required, current_user
from app.email import send_email


@main.route('/')
def hello_world():
    # send_email('1573572431@qq.com', '默默', 'main/email/confirm', name="1234")
    return 'Hello World!'


# 登录页面
@main.route('/login/', methods=['GET', 'POST'])
def LoginView():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            Email = form.Email.data
            pwa = form.pwd.data
            user1 = UserInfo.query.filter_by(Email=Email.lower()).first()
            if user1 is not None and user1.verify_password(pwa):
                session['id'] = user1.id
                # if user1.confirmed:
                login_user(user1, form.remember_me.data)
                next = request.args.get('next')
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
                # else:
                #     flash("此账号未激活")
            else:
                flash('邮箱或者密码错误！！')
        except:
            db.session.rollback()
    return render_template('main/Login.html', form=form)


# 注册页面
@main.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            Email = form.Email.data
            user = form.user.data
            pwa = form.pwa1.data
            sex = form.sex.data
            if int(sex) == 1:
                u1 = UserInfo()
                u1.Email = Email
                u1.Username = user
                u1.password = pwa
                u1.Sex = '男'
            else:
                u1 = UserInfo()
                u1.Email = Email
                u1.Username = user
                u1.password = pwa
                u1.Sex = '女'
            db.session.add(u1)
            db.session.commit()
            token = u1.generate_confirmation_token()
            send_email(u1.Email, '激活账号', 'main/email/confirm', user=u1, token=token)
            flash("有一件确认邮件已经发送到您的邮箱,请及时激活账号！！")
            return redirect(url_for('main.LoginView'))
        except:
            db.session.rollback()
    return render_template('main/registered.html', form=form)


# 注销页面
@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已成功注销')
    return redirect(url_for("main.index"))


# 修改密码
@main.route('/passupdate/', methods=['GET', 'POST'])
def PasswordChangeView():
    form = PasswordChangeForm()
    newpass = form.newpassword.data
    oldpass = form.oldpassword.data
    if form.validate_on_submit():
        try:
            t1 = UserInfo.query.filter_by(id=session['id']).first()
            if t1.verify_password(oldpass):
                t1.password = newpass
                db.session.add(t1)
                db.session.commit()
                return redirect(url_for('main.login'))
        except:
            raise RuntimeError('修改错误！！')
    return render_template('main/ChangePass.html', form= form)


# 更新邮箱
@main.route('/EmailChange/', methods=['GET', 'POST'])
def EmailChangeView():
    form = EmailChangeForm()
    email = form.Email.data
    pwd = form.password.data
    t1 = UserInfo.query.filter_by(id=session['id']).first()
    if form.validate_on_submit():
        try:
            if t1.verify_password(pwd) and t1.Email != email:
                t1.Email = email
                db.session.add(t1)
                db.session.commit()
                token = t1.generate_confirmation_token()
                send_email(t1.Email, '重置邮箱', 'main/email/confirm', user=t1, token=token)
                flash("有一件确认邮件已经发送到您的邮箱,请重置邮箱")
        except:
            raise RuntimeError("密码或者邮箱不正确")
    return render_template('main/EmailChange.html', form= form)


# 重置密码
@main.route('/ResetPassword/', methods=['GET', 'POST'])
def ResetPasswordView():
    form = ResetPasswordForm()
    email = form.Email.data
    if form.validate_on_submit():
        t1 = UserInfo.query.filter_by(Email=email).first()
        if t1.Email == email:
            token = t1.generate_confirmation_token()
            send_email(t1.Email, '重置密码密码', 'main/email/ResetPassword', user=t1, token=token)
            flash("有一件确认邮件已经发送到您的邮箱,")
        else:
            flash("邮箱不正确!")
    return render_template('main/ResetPassword/ResetEmail.html', form=form)


# 重置密码确认视图
@main.route('/ResetPasswordComfirm/', methods=['GET', 'POST'])
def ResetPasswordComfirmView():
    form = ResetPassForm()
    pwd = form.newpassword.data
    if form.validate_on_submit():
        t1 = UserInfo.query.filter_by(id=session['id']).first()
        try:
            t1.password = pwd
            db.session.add(t1)
            db.session.commit()
            flash("密码重置成功！！")
            return redirect(url_for('main.index'))
        except:
            raise RuntimeError('重置失败')
    return render_template('main/ResetPassword/ResetPass.html', form= form)


# 邮箱修改
@main.route('/updatepass/<token>')
@login_required
def ResetPassword(token):
    if current_user.confirm(token):
        db.session.commit()
        flash("填写新的密码！！")
    else:
        flash("重置失效！！")
    return redirect(url_for("main.ResetPasswordComfirmView"))


# 激活账户的视图函数
@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash("您已经激活您的账号！")
    else:
        flash("激活链接无效或已过期")
    return redirect(url_for("main.index"))


