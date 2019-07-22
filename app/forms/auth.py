#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : wangyong
# @Time    : 2019/5/7 上午8:40
# @File    : app.py

from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import EqualTo, Length, DataRequired, Email, ValidationError
from app.models.user import User
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])
    nickname = StringField(label='昵称', validators=[DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已存在')


class LoginForm(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class EmailForm(FlaskForm):
    email = StringField(label='邮箱', validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(validators=[DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)],
                              render_kw={"placeholder": "请输入密码"})
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password1', message='两次密码不一致')],
                              render_kw={"placeholder": "请确认密码"})
