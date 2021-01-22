#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:20
import os

import peewee_async

file_path=os.path.dirname(__file__)
par_path=os.path.dirname(file_path)
favicon_path=os.path.join(par_path,'static/icon.png')
oss_url='https://rngclub-1258903123.cos.ap-shanghai.myqcloud.com'


settings = {
    'debug': True,
    'static_path': os.path.join(par_path, 'static'),
    'template_path': os.path.join(par_path, 'templates'),
    "OSS_URL":oss_url,
    "secret_key":"vRSwuGcT!iE3F98p",
    "jwt_expire":7*24*3600,
    "redis":{
        "host":"127.0.0.1"
    }
}

database=peewee_async.MySQLDatabase('freehub',host='47.101.203.87',user='root',port=3306,password='newpwd',charset='utf8mb4')
