#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:18
import json
import jwt
import datetime

from RNGfreehub.handler import redisHandler, BaseHandler
from apps.users.models import TUser
from apps.users.forms import signupForm
from apps.users.forms import loginForm
from apps.credential.models import TCrendential,DoesNotExist
from apps.utils.pwdation import *
from peewee import fn
from apps.utils.hub_decorators import authenticated_async

class signup(redisHandler):
   async def get(self, *args, **kwargs):
        pass
   async def post(self, *args, **kwargs):
        re_data={}
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)
        except json.decoder.JSONDecodeError as e:
            param =None
        signup_form = signupForm.from_json(param)
        if signup_form.validate():
            credential = signup_form.credential.data
            sms_code=signup_form.sms_code.data
            nickname=signup_form.nickname.data
            password = signup_form.password.data
            email=signup_form.email.data

            #用户注册账号是否存在
            try:
                user_credential_exists=await self.application.objects.get(TCrendential,credential_name=credential)
                self.set_status(400)
                re_data['credential'] = "该账号已存在"
            except DoesNotExist as e:
                #判断验证码是否正确
                sms_validate=self.redis_conn.get("{0}_{1}".format(credential,sms_code))
                if sms_validate:
                    #t_user新增数据
                    user= await self.application.objects.create(TUser,
                                                nick_name=nickname,
                                                phone=credential,
                                                email=email
                                                )
                    #t_credential新增数据
                    salt=create_salt()
                    password_md5=create_md5(password,salt)
                    await self.application.objects.create(TCrendential,
                                                       user_id=user.id,
                                                       credential_name=credential,
                                                       password=password_md5,
                                                       salt=salt,
                                                       type=2)
                    re_data['user_id']=user.id
                else:
                    self.set_status(400)
                    re_data['code']="验证码错误或失效"
        else:
            self.set_status(400)
            for field in signup_form.errors:
                re_data[field]=signup_form.errors[field][0]
        self.finish(json.dumps(re_data))


class login(BaseHandler):
    async def get(self, *args, **kwargs):
        pass
    async def post(self, *args, **kwargs):
        re_data={}
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)
        except json.decoder.JSONDecodeError as e:
            param =None
        login_form=loginForm.from_json(param)
        if login_form.validate():
            credential = login_form.credential.data
            password = login_form.password.data
            try:
                credential_info= await TCrendential().object.get(TCrendential,credential_name=credential)
                salt=credential_info.salt
                try :
                    credential_res= await self.application.objects.get(TCrendential,credential_name =credential,password =fn.md5(password + salt))
                    user_res=await self.application.objects.get(TUser,id=credential_res.user_id)
                    payload={
                        "user_id":user_res.id,
                        "nickname":user_res.nick_name,
                        "exp":datetime.datetime.utcnow()
                    }
                    token=jwt.encode(payload,self.settings['secret_key'],algorithm='HS256')
                    re_data['id']=user_res.id
                    re_data['nick_name']=user_res.nick_name
                    re_data['avatar']=user_res.avatar
                    re_data['token']=token.decode('utf8')

                except DoesNotExist as e:
                    self.set_status(400)
                    re_data['non_fields']='账号或密码错误'
            except DoesNotExist as e:
                self.set_status(400)
                re_data['code']='账号不存在'
        else:
            self.set_status(400)
            for field in login_form.errors:
                re_data[field] = login_form.errors[field][0]

        self.finish(re_data)



class baseInfo(BaseHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data={}
        try:
            user=await self.application.objects.get(TUser,id=int(self.current_user.id))
            re_data['id']=user.id
            re_data['nick_name']=user.nick_name
            re_data['avatar']=user.avatar
        except TUser.DoesNotExist as e:
            self.set_status(400)
            re_data['user_id']='用户不存在'

        self.finish(re_data)