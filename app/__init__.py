#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : wangyong
# @Time    : 2019/5/6 下午3:39
# @File    : __init__.py

import click
from flask import Flask
from app.models.base import db
from app.models.user import User
from flask_login import LoginManager
from app.web import web
from app.extensions import mail

login_manager = LoginManager()


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


def create_app():

    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    register_blueprint(app)
    register_extension(app)

    @app.cli.command()
    def initdb():
        db.create_all()
        click.echo('Initialized database')

    return app


def register_blueprint(app):
    app.register_blueprint(web)


def register_extension(app):
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'


if __name__ == "__main__":
    app = create_app()
    print(app.debug)
    print(app.testing)
    app.run(debug=True)
