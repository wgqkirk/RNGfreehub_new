#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/20 15:13

from RNGfreehub.baseModel import baseModel
from peewee import *

class TCrendential(baseModel):
    id = AutoField(primary_key=True)
    user_id=BigIntegerField(verbose_name='用户id')
    credential_name=CharField(max_length=255,verbose_name='登录账号，可以为以下任意一种（1.用户名，2.手机号）')
    password=CharField(max_length=255,verbose_name='登录密码')
    salt=CharField(max_length=10,verbose_name='加密盐')
    type=SmallIntegerField(verbose_name='登录方式（1：用户名，2：手机号）')
    is_confirmed_phone=SmallIntegerField(default=0,verbose_name='手机号验证（0：否，1：是）')
    is_confirmed_email=SmallIntegerField(default=0,verbose_name='email验证（0：否，1：是）')
    is_reset_password=SmallIntegerField(default=0,verbose_name='是否重置过密码（0：否，1：是）')


    class Meta():
        table_name='t_credential'