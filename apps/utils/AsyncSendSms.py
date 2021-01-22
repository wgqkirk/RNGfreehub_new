#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/28 11:59
import json
from urllib.parse import urlencode
from tornado import httpclient
from tornado.httpclient import HTTPRequest

from hashlib import sha256
import time

class AsyncSendSms:
    def __init__(self):
        # 短信应用SDK AppID
        self.appid = 1400196961  # SDK AppID是1400开头
        # 短信应用SDK AppKey
        self.appkey = "788dbfd4ea841a657772b2eaebed34e9"

        # 短信模板ID，需要在短信应用中申请
        self.template_id = 303096
        # 签名
        self.sms_sign ="梨园月河"

    async def send_single_sms(self,phone_numbers,code):
        http_client=httpclient.AsyncHTTPClient()



        strMobile = phone_numbers
        strAppKey = self.appkey
        strRand = code
        strTime = int(time.time())
        sig = sha256(('appkey={0}&random={1}&time={2}&mobile={3}'.format(strAppKey,strRand,strTime, strMobile)).encode('utf-8'))
        sig=sig.hexdigest()
        url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid={0}&random={1}'.format(self.appid,strRand)
        data = {
            "ext": "",
            "extend": "",
            "params": ['登录',strRand,5],
            "sig": sig,
            "sign": self.sms_sign,
            "tel": {"mobile": strMobile,"nationcode": "86"},
            "time": strTime,
            "tpl_id": self.template_id
        }
        post_request=HTTPRequest(url=url,method='POST',body=json.dumps(data))

        res=await http_client.fetch(post_request)
        return json.loads(res.body.decode("utf8"))