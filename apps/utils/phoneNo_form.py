#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/28 13:33
from wtforms.fields import StringField
from wtforms.validators import *
from wtforms_tornado import Form

class sendSmsForm(Form):
    credential = StringField('手机号',validators=[
        data_required(message='手机号不能为空！'),
        regexp(regex='^[1][3,4,5,7,8][0-9]{9}$',message='手机号不合法')
    ])