#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:20
import base64

import urllib.parse

from tornado.httpclient import HTTPRequest
from tornado import httpclient
import requests
import os
import hashlib

from apps.hub.test import get_auth

class upload_file():

    async def upload(self,file_name,file_type,byte_data):
        http_client = httpclient.AsyncHTTPClient()

        if file_type=='avatar':
            #头像文件
            bucket_url='/avatar/'
        elif file_type=='image':
            #普通图片
            bucket_url = '/media/image/'
        elif file_type=='video':
            #视频文件
            bucket_url = '/media/video/'
        else:
            #其他文件
            bucket_url = '/other/'

        md5_1 = hashlib.md5()  # 创建一个md5算法对象
        md5_1.update(byte_data)
        Length = len(byte_data)
        file_md5 = base64.b64encode(md5_1.digest()).decode('utf-8')

        HttpHeaders = 'content-md5' + '=' + urllib.parse.quote('{}'.format(file_md5),
                                                               safe='') + '&' + 'host' + '=' + urllib.parse.quote(
            'rngclub-1258903123.cos.ap-shanghai.myqcloud.com')

        Authorization = get_auth(HttpHeaders=HttpHeaders, HttpURI='{}{}'.format(bucket_url,file_name))

        headers = {'Host': 'rngclub-1258903123.cos.ap-shanghai.myqcloud.com', 'Authorization': Authorization,
                   'Content-MD5': file_md5, 'Content-Length': str(Length)}

        url = 'https://rngclub-1258903123.cos.ap-shanghai.myqcloud.com{}{}'.format(bucket_url, file_name)

        # post_request = HTTPRequest(url=url, method='put', headers=headers, body=byte_data)
        # res = await http_client.fetch(post_request)


        res =requests.put(
            'https://rngclub-1258903123.cos.ap-shanghai.myqcloud.com{}{}'.format(bucket_url, file_name),
            headers=headers, data=byte_data)
        if res.status_code==200:
            return bucket_url + file_name
        else:
            return 'error'