#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/21 11:07
import datetime
import hashlib
import json
import redis
import time

from tornado.web import RequestHandler
from apps.hub.models import TStreet
from apps.utils.AsyncSendSms import AsyncSendSms
from apps.utils.getSixRandomNum import get_random_code
from apps.utils.pageation import page_help
from apps.utils.phoneNo_form import sendSmsForm


class BaseHandler(RequestHandler):
    """
    基本handler，设置可访问的请求头
    """
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')
    def options(self, *args, **kwargs):
        """
        处理跨域请求
        :param args:
        :param kwargs:
        :return:
        """
        pass

class redisHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        """
        设置Redis的连接
        :param application:
        :param request:
        :param kwargs:
        """
        super().__init__(application, request, **kwargs)
        self.redis_conn=redis.StrictRedis(**self.settings['redis'])




class single_topic(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('single-topic.html')


class errorPageHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('error404.html')


class sms(redisHandler):
    async def get(self, *args, **kwargs):
        self.set_status(405)

    async def post(self, *args, **kwargs):
        re_data = {}
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)
        except json.decoder.JSONDecodeError as e:
            param = None
        sms_form =sendSmsForm.from_json(param)
        if sms_form.validate():
            try:
                phone=sms_form.credential.data
                code=get_random_code()
                one_min_expire=self.redis_conn.get("{0}_{1}".format(phone,'busy'))
                day_count=self.redis_conn.get("{0}_{1}".format(phone,'send_count'))
                if not day_count:
                    day_count=0
                day_count=int(day_count)
                if one_min_expire:
                    re_data['non-feild']='请等一分钟后再试'
                    self.set_status(400)
                else:
                    if day_count>=10:
                        re_data['non-feild']='一天最多发送十次'
                        self.set_status(400)
                    else:
                        day_count+=1
                        send=AsyncSendSms()
                        res=await send.send_single_sms(phone,code)
                        if res['result']==0:
                            self.redis_conn.set("{0}_{1}".format(phone,code),1,5*60)
                            self.redis_conn.set("{0}_{1}".format(phone,'busy'),1,1*60)
                            self.redis_conn.set("{0}_{1}".format(phone,'send_count'),day_count,int(time.mktime(time.strptime(datetime.datetime.now().strftime('%Y-%m-%d')+' 23:59:59','%Y-%m-%d %H:%M:%S'))-time.time()))
                            re_data['code']='ok'
            except Exception as e:
                self.set_status(400)
                re_data['code']='未知错误，请重试'
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field]=sms_form.errors[field][0]
        self.finish(re_data)