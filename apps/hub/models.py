#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/20 17:18

from RNGfreehub.baseModel import baseModel
from peewee import *

class TStreet(baseModel):
    id = AutoField(primary_key=True)
    post_id= BigIntegerField(verbose_name='主题帖标识ID')
    title=CharField(max_length=255,verbose_name='主题帖标题',null=False)
    post_url=CharField(max_length=255,verbose_name='主题帖url')
    author=CharField(max_length=255,verbose_name='po主名')
    author_url=CharField(max_length=255,verbose_name='po主主页url')
    create_date=DateField(formats='%Y-%m-%d',verbose_name='主题帖创建日期')
    light_count=IntegerField(verbose_name='亮帖数')
    reply_num=IntegerField(verbose_name='回复数量')
    page_views=IntegerField(verbose_name='浏览量')
    last_reply_time=CharField(max_length=255,verbose_name='最后回复时间')
    last_reply_user=CharField(max_length=255,verbose_name='最后回复用户')

    class Meta():
        table_name='t_street'

class TPost(baseModel):
    id=AutoField(primary_key=True)
    title=CharField(max_length=50,verbose_name='标题')
    content=TextField(verbose_name='内容')
    reply_count=IntegerField(verbose_name='回复数')
    last_reply_user_id=BigIntegerField(verbose_name='最后回复人id')
    last_reply_time=DateTimeField(formats='%Y-%m-%d %H:%M:%S',verbose_name='最后回复时间')
    ip=CharField(verbose_name='发帖人ip')

    class Meta():
        table_name='t_post'


class TPostPic(baseModel):
    id = AutoField(primary_key=True)
    post_id = BigIntegerField(verbose_name='帖子id')
    url = CharField(max_length=255,verbose_name='图片url')
    seq = IntegerField(default=1,verbose_name='顺序')

    class Meta():
        table_name = 't_post_pic'


class TPostTag(baseModel):
    id = AutoField(primary_key=True)
    post_id = BigIntegerField(verbose_name='帖子id')
    tag_id = BigIntegerField(verbose_name='标签id')

    class Meta():
        table_name = 't_post_tag'


class TTagGroup(baseModel):
    id=AutoField(primary_key=True)
    tag_group_name=CharField(max_length=255,verbose_name='标签组名称',null=False)

    class Meta():
        table_name='t_tag_group'


class TTag(baseModel):
    id=AutoField(primary_key=True)
    tag_name=CharField(max_length=255,verbose_name='标签名称',null=False,unique=True)
    color=CharField(max_length=32,verbose_name='颜色',default='#FFFFFF')
    description=CharField(max_length=255,verbose_name='简介')
    tag_group_id=BigIntegerField(verbose_name='标签组id')

    class Meta():
        table_name='t_tag'


class TPostTag(baseModel):
    id = AutoField(primary_key=True)
    post_id = BigIntegerField(verbose_name='帖子id')
    tag_id = BigIntegerField( verbose_name='标签id')
    tag_name = CharField(max_length=255, verbose_name='标签名称', null=False)

    class Meta():
        table_name='t_post_tag'

class TPostLike(baseModel):
    # 帖子点赞
    id = AutoField(primary_key=True)
    user_id = BigIntegerField(verbose_name="用户id")
    post_id = BigIntegerField(verbose_name="帖子id")

    class Meta():
        table_name='t_post_like'

class TPostReply(baseModel):
    # 评论和回复
    id = AutoField(primary_key=True)
    post_id = BigIntegerField(null=True, verbose_name="帖子id，只有评论才会有值")
    target_user_id=BigIntegerField(null=False,verbose_name='回复目标用户id')
    reply_user_id = BigIntegerField(verbose_name="回复评论用户id")
    ip = CharField(verbose_name='发帖人ip')
    reply_user_name = CharField(max_length=32,verbose_name="回复评论用户昵称")
    reply_parent_id = BigIntegerField(null=True, verbose_name="回复的评论id，只有回复才会有值")
    reply_user_id = BigIntegerField(verbose_name="回复的父id")
    content = CharField(max_length=1000, verbose_name="回复评论内容")
    reply_nums = IntegerField(default=0, verbose_name="回复数")
    like_nums = IntegerField(default=0, verbose_name="点赞数")
    is_read = IntegerField(default=0,verbose_name="是否已读（0：未读，1：已读）")
    class Meta():
        table_name='t_post_reply'


class TReplyLike(baseModel):
    # 评论点赞
    id = AutoField(primary_key=True)
    user_id = BigIntegerField(verbose_name="用户id")
    post_reply_id = BigIntegerField(verbose_name="评论id")

    class Meta():
        table_name='t_reply_like'