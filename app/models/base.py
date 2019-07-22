#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : wangyong
# @Time    : 2019/5/6 下午3:53
# @File    : base.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        """
        使用@contextmanage创建上下文管理器，实现数据库的自动保存和回滚
        :return:
        """
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        """
        重写Query方法，以实现一些默认操作，比如status=1表示只查询未删除(使用status实现假删除)的记录
        :param kwargs:
        :return:
        """
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    """
    __abstract__告诉SQLAlchemy不要生成数据表,Base只用于被继承
    Base类定义两个所有模型都必须的:
        create_time 添加时间
        status 用于假删除
    set_attrs避免错误属性赋值
    """
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # 实现存储时间戳，展示格式化时间
    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    # 假删除
    def delete(self):
        self.status = 0
