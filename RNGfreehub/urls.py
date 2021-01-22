#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:20
from apps.users import urls as user_userl
from apps.credential import urls as credential_urls
from apps.hub import urls as hub_urls


from RNGfreehub.handler import *
from apps.users.handler import *
from apps.hub.handler import *

page_url=[
    (r'/api/v1/sendSms/',sms),
    (r'^/user/baseInfo/',baseInfo),


    (r'^/postList',postlist),
    (r'^/postList/top7',postlist_top7),
    (r'^/post/([0-9]+)/',posting),
    (r'^/post',posting),
    (r'^/postDeepInfo/([0-9]+)/',postDeepInfo),

    (r'^/post/([0-9]+)/comment/',post_comment),
    (r'^/comment/([0-9]+)/reply/',comment_reply),

    (r'^/post/notice/', notice),

    (r'^/taglist',taglist),
    (r'^/tag/([0-9]+)',tag),
    (r'^/tag',tag),

    (r'^/single-topic/',single_topic),
    (r'^/signup/',signup),
    (r'^/login/',login),

    (r'.*',errorPageHandler),
]