#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/4/3 17:34

from wtforms.fields import StringField
# from wtforms.validators import Required
from wtforms.validators import *
from wtforms_tornado import Form

class postForm(Form):
    title = StringField('标题', validators=[
        data_required(message='标题不能为空！'),
        length(min=1,max=255, message='标题长度不合法')
    ])
    content = StringField('正文', validators=[
        data_required(message='正文不能为空！'),
        length(min=1, max=65530, message='正文长度不合法!')
    ])


class tagForm(Form):
    tag_group_id= StringField('标签组id',validators=[
        data_required(message='标签不能为空!')
    ])

    tag_name=StringField('标签名', validators=[
        data_required(message='标签名不能为空！'),
        length(min=1,max=15, message='标签名长度不合法')
    ])

    color = StringField('颜色', validators=[
        regexp(regex="^#\S{6}$",message='颜色16进制不合法')
    ])

    description=StringField('标签简介',validators=[
        length(min=0, max=500, message='简介不能超过500字')
    ])


class commentForm(Form):
    content=StringField('回复评论内容', validators=[
        data_required(message='回复评论内容不能为空！'),
        length(min=1,max=1000, message='回复评论长度不合法')
    ])

class replyForm(Form):
    post_id=StringField('帖子id', validators=[
        data_required(message='帖子id不能为空！')
    ])

    content=StringField('回复评论内容', validators=[
        data_required(message='回复评论内容不能为空！'),
        length(min=1,max=1000, message='回复评论长度不合法')
    ])