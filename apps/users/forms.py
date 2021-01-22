#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/25 16:09

from wtforms.fields import StringField
# from wtforms.validators import Required
from wtforms.validators import *
from wtforms_tornado import Form

class loginForm(Form):
    credential = StringField('账号',validators=[
        data_required(message='账号不能为空！'),
        regexp(regex='^[1][3,4,5,7,8][0-9]{9}$',message='手机号不合法')
    ])
    password = StringField('密码',validators=[
        data_required(message='密码不能为空！'),
        length(min=6,max=15,message='长度不合法!')
    ])

class signupForm(Form):
    credential = StringField('账号',validators=[
        data_required(message='账号不能为空！'),
        regexp(regex='^[1][3,4,5,7,8][0-9]{9}$',message='手机号不合法')
    ])

    sms_code = StringField('验证码', validators=[
        data_required(message='验证码不能为空！'),
        length(min=6, max=6, message='验证码长度不合法')
    ])

    nickname = StringField('昵称', validators=[
        data_required(message='昵称不能为空！'),
        length(min=2,max=10,message='昵称长度不合法')
    ])

    email=StringField('邮箱',validators=[
        data_required(message='邮箱不能为空'),
        Email(message='邮箱不合法')
    ])

    password = StringField('密码',validators=[
        data_required(message='密码不能为空！'),
        length(min=8,max=15,message='长度不合法!')
    ])