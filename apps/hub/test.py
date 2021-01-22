#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:20

import hashlib, hmac, time

def get_auth(HttpHeaders,HttpURI='',HttpParameters=''):
    # 密钥参数
    secret_id = "AKIDg7LVR7aq0ve9WiLVAfv2xc5LNAlErUM2"
    secret_key = "f9OPJ1ZsyrV6YmneGfw3xc5Wvtc8SYQ4"
    HttpMethod = 'put'
    algorithm = "sha1"
    timestamp_start = int(time.time())
    timestamp_end = timestamp_start + 3600
    key_time=str(timestamp_start)+';'+str(timestamp_end)
    httpstring = HttpMethod + '\n' + HttpURI+'\n'+HttpParameters+'\n'+ HttpHeaders+'\n'
    sha1_http_string= hashlib.sha1(httpstring.encode('utf-8')).hexdigest()
    StringToSign=algorithm+'\n'+key_time+'\n'+sha1_http_string+'\n'
    sign_key = hmac.new(secret_key.encode('utf-8'), key_time.encode('utf-8'), hashlib.sha1).hexdigest()
    signature=hmac.new(sign_key.encode('utf-8'),StringToSign.encode('utf-8'), hashlib.sha1).hexdigest()

    #拼接 Authorization
    authorization = ("q-sign-algorithm=" +
                     algorithm + "&" +
                     "q-ak=" + secret_id + "&" + "q-sign-time=" + key_time + "&" +
                     "q-key-time=" + key_time + "&" + 'q-header-list=content-md5;host&q-url-param-list=' + "&" + "q-signature=" + signature)
    return authorization
