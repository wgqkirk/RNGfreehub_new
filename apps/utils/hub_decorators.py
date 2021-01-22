#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/4/2 14:07

import functools
import jwt
from apps.users.models import TUser,DoesNotExist


def authenticated_async(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        tsessionid=self.request.headers.get('tsessionid',None)
        if tsessionid:
            try:
                send_data=jwt.decode(tsessionid,self.settings['secret_key'],leeway=self.settings["jwt_expire"],options={"verify_exp": True})
                user_id=send_data['user_id']
                try:
                    user=await self.application.objects.get(TUser,id=user_id)
                    self._current_user=user

                    #...
                    await method(self, *args, **kwargs)
                except DoesNotExist as e:
                    self.set_status(401)
                    self.finish({'error':"请先登录！"})
            except jwt.ExpiredSignatureError as e:
                self.set_status(401)
                self.finish({'error':"请先登录！"})
        else:
            self.set_status(401)
            self.finish({'error':"请先登录！"})


    return wrapper