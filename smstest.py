#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/26 16:11
from random import choice
from hashlib import sha256
import time
import requests
import json

class sendSms():
    def __init__(self):
        # 短信应用SDK AppID
        self.appid = 1400196961  # SDK AppID是1400开头
        # 短信应用SDK AppKey
        self.appkey = "788dbfd4ea841a657772b2eaebed34e9"

        # 短信模板ID，需要在短信应用中申请
        self.template_id = 303096  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
        # 签名
        self.sms_sign ="梨园月河"


    def send_sms(self,phone_numbers):

        """
        发送单条短信
        :return:
        """
        def get_random_code():
            first_chars = '132465789'
            chars = '1234567890'
            length = 6
            len_chars = len(chars) - 1
            code = ''
            code = choice(first_chars)
            for i in range(length - 1):
                # 每次从chars中随机取一位
                code += choice(chars)
            return code

        strMobile = phone_numbers
        strAppKey = self.appkey
        strRand = get_random_code()
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
        res=requests.post(url,json=data)
        return res.content

if __name__ == '__main__':
    send=sendSms()
    send.send_sms(18621544352)