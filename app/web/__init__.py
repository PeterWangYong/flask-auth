#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : wangyong
# @Time    : 2019/5/6 下午3:42
# @File    : __init__.py

from flask.blueprints import Blueprint

web = Blueprint('web', __name__)

from app.web import auth
