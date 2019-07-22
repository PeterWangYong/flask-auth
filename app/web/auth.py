#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : wangyong
# @Time    : 2019/5/7 上午10:35
# @File    : app.py

from flask import request, redirect, url_for, render_template, flash, current_app
from . import web
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from flask_login import login_user, logout_user
from app.models.user import User
from app.models.base import db
from app.extensions import mail
from flask_mail import Message
from threading import Thread


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        flash('注册成功')
        return redirect(url_for('web.login'))
    return render_template('register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for('web.index')
            return redirect(next_url)
        else:
            flash('账号不存在或密码错误')
    return render_template('login.html', form=form)


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@web.route('/')
def index():
    return render_template('index.html', user={})


@web.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    form = EmailForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash('账号不存在')
        else:
            send_mail(form.email.data, '重置你的密码',
                      'email_reset_password.html', user=user,
                      token=user.generate_token())
            flash('邮件已发送，请查收')
    return render_template('forget_password.html', form=form)


@web.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm(request.form)
    if form.validate_on_submit():
        if User.reset_password(token, form.password1.data):
            flash('密码重置成功，请登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('reset_password.html', form=form)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    mail.send(msg)
    thread = Thread(target=send_async_mail, args=[app, msg])
    thread.start()


def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
