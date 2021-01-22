#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/20 13:27
import datetime
import asyncio
from peewee import *
import peewee_async
from RNGfreehub.settings import database

class baseModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """将事务改成atomic_async"""
        self.trans = database.atomic_async
        """添加一个Manager类"""
        self.object = peewee_async.Manager(database)

    cr_user_id = BigIntegerField(default=None)
    cr_date = DateTimeField(formats='%Y-%m-%d %H:%M:%S')
    op_user_id = BigIntegerField(default=None)
    op_date= DateTimeField(formats='%Y-%m-%d %H:%M:%S')
    del_tag = SmallIntegerField(default=0)
    version = IntegerField(default=1)

    class Meta:
        database=database