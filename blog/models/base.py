# coding = utf-8
from contextlib import contextmanager
from datetime import datetime, timezone,timedelta

from flask_sqlalchemy import BaseQuery
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        # kwargs.get('status', default=1)
        return super(Query, self).filter_by(**kwargs)


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True  # 不创建Base表
    create_time = Column('create_time', Integer, default=int(datetime.utcnow().timestamp()))
    status = Column(SmallInteger, default=1)

    # 基类设置__init__()后不能不能接受参数赋值，意味着不能再用类似user=User(key=value)的方法创建数据库，需要用重写的set_attrs方法赋值。！！！
    # todo 正常上线需要启用__init__()函数。
    # def __init__(self):
    #     self.create_time = int(datetime.now().timestamp())
    #
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time) + timedelta(days=-8,hours=8)
        else:
            return None
