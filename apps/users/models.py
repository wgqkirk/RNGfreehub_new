#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:19

from peewee import *
from RNGfreehub.baseModel import baseModel

class TUser(baseModel):
    id=AutoField(primary_key=True)
    nick_name=CharField(max_length=255,unique=True,verbose_name='昵称')
    real_name=CharField(max_length=32,verbose_name='真实姓名')
    avatar=CharField(max_length=255,verbose_name='头像url')
    birth=DateField(formats='%Y-%m-%d',verbose_name='出生日期')
    id_card_no=CharField(max_length=64,verbose_name='身份证号')
    phone=CharField(max_length=32,verbose_name='手机号')
    email=CharField(max_length=255,verbose_name='邮箱')
    gender=SmallIntegerField(default=0,verbose_name='性别')

    class Meta():
        table_name='t_user'
