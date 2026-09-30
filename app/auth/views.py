import hashlib

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required

from . import auth
from .. import db
from ..email_util import send_email
from ..models import User, Role
import random
from datetime import datetime, timedelta
from app.models import PasswordResetCode
from app.auth.forms import PasswordResetCodeForm
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ChangeEmailForm, PasswordResetRequestForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user=user, remember=form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码错误。')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('已退出登录。')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        user.role = user.role = Role.query.filter_by(name='User').first()
        db.session.add(user)
        user.follow(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('确认邮件已发送至你的邮箱，请前往邮箱查看。')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('账号激活成功！')
    else:
        flash('账号确认链接无效或者已经过期，请重新发送确认邮件。')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    user = current_user
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html',user=user)

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('新的确认邮件已发送至你的邮箱。')
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            current_user.password = form.new_password.data
            db.session.commit()  # 提交到数据库，更新密码
            logout_user()
            flash('密码修改成功！请使用新密码重新登录。')
            return redirect(url_for('auth.login'))
        else:
            flash('旧密码输入错误，请重新输入！')
    return render_template('auth/change_password.html', form=form)

@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        token = current_user.generate_change_email_token(form.new_email.data)
        send_email(form.new_email.data, '确认修改邮箱',
                   'auth/email/change_email', user=current_user, token=token)
        flash('一封确认邮件已经发送到你的新邮箱，请前往点击链接完成修改。')
        return redirect(url_for('main.index'))
    return render_template('auth/change_email_request.html', form=form)


@auth.route('/change-email/<token>')
@login_required
def change_email_confirm(token):
    if current_user.change_email(token):
        db.session.commit()
        logout_user()
        flash('邮箱修改成功！请使用新邮箱登录。')
    else:
        flash('链接无效，或者已经过期。')
    return redirect(url_for('main.index'))

# 验证码找回密码：第一步，填写邮箱，发送验证码
@auth.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            code = ''.join(random.choices('0123456789', k=6))
            expire = datetime.utcnow() + timedelta(minutes=10)
            PasswordResetCode.query.filter_by(user_id=user.id).delete()
            new_code_record = PasswordResetCode(user_id=user.id, code=code, expire_time=expire)
            db.session.add(new_code_record)
            db.session.commit()
            send_email(user.email, '账号密码重置验证码', 'auth/email/reset_password', code=code, user=user)
        flash('验证码邮件已发送，请查收，有效期10分钟。')
        return redirect(url_for('auth.password_reset_verify', email=form.email.data))
    return render_template('auth/password_reset_request.html', form=form)

@auth.route('/password_reset_verify', methods=['GET', 'POST'])
def password_reset_verify():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('邮箱参数错误，请重新发起重置')
        return redirect(url_for('auth.password_reset_request'))

    form = PasswordResetCodeForm()
    if form.validate_on_submit():
        record = PasswordResetCode.query.filter_by(user_id=user.id, code=form.code.data).first()
        if record and record.expire_time > datetime.utcnow():
            user.password = form.new_password.data
            db.session.delete(record)
            db.session.commit()
            flash('密码重置成功！请使用新密码登录。')
            return redirect(url_for('auth.login'))
        else:
            flash('验证码错误或者已过期！')
    return render_template('auth/password_reset_verify.html', form=form)
