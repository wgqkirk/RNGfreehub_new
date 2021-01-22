#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 14:57
import json
from functools import partial

from apps.utils.phoneNo_form import sendSmsForm
from apps.utils.AsyncSendSms import AsyncSendSms
from tornado.web import RequestHandler
from RNGfreehub.handler import redisHandler
from apps.utils.getSixRandomNum import get_random_code

class sms(redisHandler):
    async def get(self, *args, **kwargs):
        self.write('111')

    async def post(self, *args, **kwargs):

        data=self.get_arguments('phone')
        data={'phone':data}
        sms_form=sendSmsForm(data)
        if sms_form.validate():
            try:
                phone=sms_form.phone.data
                code=get_random_code()
                send=AsyncSendSms()
                res=await send.send_single_sms(phone,code)
                if res['result']==0:
                    self.write(json.dumps({'phone':phone,'code':0}))
                    self.redis_conn.set("{0}_{1}".format(phone,code),1,5*60)
                    self.redis_conn.set("{0}_{1}".format(phone,code),1,5*60)
                    self.redis_conn.set("{0}_{1}".format(phone,code),1,5*60)
            except Exception as e:
                self.write(json.dumps({'phone': phone, 'code':-1}))
        else:
            self.set_status(400)
            self.write(sms_form.errors)
