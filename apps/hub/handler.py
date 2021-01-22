#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/27 10:18
import datetime
import json
import uuid
import os

import aiofiles

from peewee import DoesNotExist,IntegrityError
from RNGfreehub.handler import BaseHandler

from apps.hub.models import TPost,TPostPic,TTag,TTagGroup,TPostReply,TPostLike
from apps.users.models import TUser
from apps.utils.hub_decorators import authenticated_async
from apps.hub.forms import *
from apps.utils.util_func import json_serial
from playhouse.shortcuts import model_to_dict

from apps.credential.AsyncUpload import *

#获取帖子列表
class postlist(BaseHandler):
    async def get(self,*args, **kwargs):
        current_page = int(self.get_argument('pagenum', 1))
        limit_num = int(self.get_argument('pagesize', 20))
        total=await self.application.objects.count(TPost.select())
        posts = await self.application.objects.execute(
            TPost.select(TPost.id,TPost.title,TUser.nick_name,TUser.avatar,TPost.reply_count,TPost.cr_date).join(TUser,on=(TPost.cr_user_id==TUser.id)).order_by(TPost.id.desc()).limit(limit_num).offset(limit_num * (current_page-1)))
        post_list = []
        for post in posts:
            post_data = {}
            post_data['id'] = post.id
            post_data['title'] = post.title
            post_data['author'] = post.tuser.nick_name
            post_data['avatar'] = post.tuser.avatar
            post_data['reply_num'] = post.reply_count
            post_data['create_date'] = post.cr_date.strftime("%m-%d %H:%M")

            post_list.append(post_data)
        data = {'total': total, 'list': post_list}
        street_list = {'code': 0, 'data': data, 'message': ''}
        re_data={
            'street_list':street_list,
        }
        self.finish(re_data)

    async def post(self, *args, **kwargs):
        pass

#获取热门帖子列表
class postlist_top7(BaseHandler):
    async def get(self,*args, **kwargs):
        re_data={}
        posts = await self.application.objects.execute(
            TPost.select(TPost.id,TPost.title,TUser.nick_name,TUser.avatar,TPost.reply_count,TPost.cr_date).join(TUser,on=(TPost.cr_user_id==TUser.id)).where(TPost.cr_date > (datetime.datetime.now()+datetime.timedelta(days=-5)).strftime("%Y-%m-%d %H:%M:%S")).order_by(TPost.reply_count.desc()).limit(7))
        post_list = []
        for post in posts:
            post_data = {}
            post_data['id']=post.id
            post_data['title']=post.title
            post_data['author']=post.tuser.nick_name
            post_data['avatar']=post.tuser.avatar
            post_data['reply_num']=post.reply_count
            post_data['create_date']=post.cr_date.strftime("%Y-%m-%d %H:%M")
            post_list.append(post_data)
        data = {'list': post_list}
        street_list = {'code': 0, 'data': data, 'message': ''}

        re_data['street_list']=street_list
        self.finish(re_data)

    async def post(self, *args, **kwargs):
        pass


#获取帖子详情、新增帖子
class posting(BaseHandler):
    async def get(self,post_id,*args, **kwargs):
        """
        获取单个帖子详情
        :param post_id:
        :param args:
        :param kwargs:
        :return:
        """
        re_data={}
        post_detail_query=TPost.select(TPost.id,TPost.title,TPost.content,TUser.nick_name,TUser.avatar,TPost.cr_date,TPost.reply_count).join(TUser,on=(TPost.cr_user_id==TUser.id)).filter(TPost.id==int(post_id))

        try:
            postdetial = await self.application.objects.execute(post_detail_query)
            for post in postdetial:
                like_count= await self.application.objects.count(TPostLike.select().where(TPostLike.post_id==int(post.id)))
                re_data={
                    "id":post.id,
                    "author":post.tuser.nick_name,
                    "avatar":post.tuser.avatar,
                    "title":post.title,
                    "content":post.content,
                    "cr_date":post.cr_date.strftime('%Y-%m-%d %H:%M'),
                    "like_count":like_count,
                    "reply_count":post.reply_count

                }
        except DoesNotExist as e:
            self.set_status(401)
            re_data['error']='该资源不存在'
        self.finish(re_data)


    @authenticated_async
    async def post(self, *args, **kwargs):
        """
        新增帖子
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        re_data={}
        remote_ip=self.request.remote_ip
        post_form=postForm(self.request.body_arguments)
        if post_form.validate():
            #是个list
            pic_meta=self.request.files.get('front_image',None)
            if pic_meta:
                # 完成图片保存并将值设置给对应的记录
                # 通过aiofiles写文件
                # 1. 文件名
                new_filename = ""
                file_list=[]
                for meta in pic_meta:
                    filename = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    type=meta.content_type.split('/')[0]
                    upload_cos=upload_file()
                    file_url = await upload_cos.upload(new_filename, type, meta['body'])
                    if file_url !='error':
                        file_list.append({"type":type,'file_name':new_filename,'file_url':file_url})
                    else:
                        self.set_status(400)
                        re_data['file']='文件上传失败'
                        self.finish(re_data)
            title=post_form.title.data
            content=post_form.content.data
            ip=remote_ip
            cr_user_id = self.current_user.id
            newpost=await self.application.objects.create(TPost,title=title,content=content,ip=ip,cr_user_id=cr_user_id,cr_date=datetime.datetime.now(),op_date=datetime.datetime.now())
            #存帖子图片
            if pic_meta:
                for seq,post_pic in enumerate(file_list,1):
                    newpostpic=await self.application.objects.create(TPostPic,post_id=newpost.id,url=self.settings['OSS_URL']+post_pic['file_url'],seq=seq,cr_user_id=cr_user_id)

            re_data['id']=newpost.id
            re_data['title']=newpost.title
            re_data['content']=newpost.content
            re_data['create_user_id']=newpost.cr_user_id
            re_data['create_time']=newpost.cr_date
            re_data['update_time']=newpost.op_date
        else:
            self.set_status(401)
            for feild in post_form.errors:
                re_data[feild]=post_form.errors[feild][0]

        self.finish(json.dumps(re_data,default=json_serial))

#帖子特殊信息
class postDeepInfo(BaseHandler):
    async def get(self, post_id,*args, **kwargs):
        re_data={}
        try:
            post=await self.application.objects.get(TPost,id=int(post_id))
            user=await self.application.objects.get(TUser,id=post.cr_user_id)
            like_count = await self.application.objects.count(
                TPostLike.select().where(TPostLike.post_id == int(post_id)))
            join_user_num = await self.application.objects.count(
                TPostReply.select().where(TPostReply.post_id == int(post_id)).group_by(TPostReply.reply_user_id))

            re_data["create_user"]={
                    "nickname": user.nick_name,
                    "avatar": user.avatar,
                    "created_date": (datetime.datetime.now() - post.cr_date).days
                }

            last_reply_user=await self.application.objects.get(TUser,id=post.last_reply_user_id)
            re_data["post_info"]={
                    "last_reply_user_id":post.last_reply_user_id,
                    "last_reply_user_name":last_reply_user.nick_name,
                    "last_reply_user_avatar":last_reply_user.avatar,
                    "last_reply_time": (datetime.datetime.now() - post.last_reply_time).seconds//3600,
                    "reply_num":post.reply_count,
                    "view_num":100,
                    "join_user_num":join_user_num,
                    "like_num":like_count,
                    }



        except TPost.DoesNotExist as e:
            self.set_status(400)
            re_data['post_id']='资源不存在'
        except TUser.DoesNotExist as e:
            re_data["post_info"]={
                "last_reply_user_id": None,
                "last_reply_user_name": None,
                "last_reply_user_avatar": None,
                "last_reply_time": None,
                "reply_num": post.reply_count,
                "view_num": 100,
                "join_user_num": join_user_num,
                "like_num": like_count,
            }

        self.finish(re_data)


    async def post(self, *args, **kwargs):
        pass


#获取标签列表
class taglist(BaseHandler):
    async def get(self, *args, **kwargs):
        current_page = int(self.get_argument('pagenum', 1))
        limit_num = int(self.get_argument('pagesize', 20))
        total = await self.application.objects.count(TTag.select())
        tags = await self.application.objects.execute(
            TTag.select().limit(limit_num).offset(limit_num * (current_page - 1)))
        tag_list = []
        for tag in tags:
            tag_data = {}
            tag_data['id'] = tag.id
            tag_data['post_id'] = tag.tag_name
            tag_data['title'] = tag.color
            tag_data['desc'] = tag.description
            tag_list.append(tag_data)

        re_data = {
            'tag_list': tag_list,
        }
        self.finish(json.dumps(re_data, default=json_serial))

    async def post(self, *args, **kwargs):
        pass


#新增标签，获取标签详情
class tag(BaseHandler):
    async def get(self, tag_id, *args, **kwargs):
        re_data = {}
        tag_detail_query = TTag.select(TTag.id, TTag.tag_name, TTag.description, TTagGroup.tag_group_name).join(
            TTagGroup, on=(TTag.tag_group_id == TTagGroup.id)).filter(TTag.id == tag_id)

        try:
            tagdetial = await self.application.objects.execute(tag_detail_query)
            for tag in tagdetial:
                re_data = {
                    "id": tag.id,
                    "name": tag.tag_name,
                    "desc": tag.description,
                    "content": tag.ttaggroup.tag_group_name
                }
        except DoesNotExist as e:
            self.set_status(401)
            re_data['error'] = '该资源不存在'
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, *args, **kwargs):
        re_data = {}
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)
        except json.decoder.JSONDecodeError as e:
            param = None
        tag_form = tagForm.from_json(param)
        if tag_form.validate():
            tag_name=tag_form.tag_name.data
            tag_group_id=tag_form.tag_group_id.data
            color=tag_form.color.data
            description=tag_form.description.data

            try:
                tag_group_exists=await self.application.objects.get(
                TTagGroup,id=tag_group_id

            )
                try:
                    tag_model = await self.application.objects.create(
                        TTag, tag_name=tag_name, tag_group_id=tag_group_id, color=color, description=description
                    )
                    new_tag_id = tag_model.id
                    re_data['tag_id']=new_tag_id
                except IntegrityError as e:
                    self.set_status(400)
                    re_data['tag_name']='标签已存在'

            except DoesNotExist as e:
                self.set_status(400)
                re_data['tag_group_id']='标签组不存在'

        else:
            self.set_status(400)
            for field in tag_form.errors:
                re_data[field] = tag_form.errors[field][0]
        self.finish(json.dumps(re_data))



#
# class reply(BaseHandler):
#     async def get(self, *args, **kwargs):
#
#
#     async def post(self, *args, **kwargs):
#         pass


class post_comment(BaseHandler):
    #评论列表
    async def get(self,post_id, *args, **kwargs):
        re_data={}
        commentList=[]
        try:
            post=await self.application.objects.get(TPost,id=post_id)
            reply_list=await self.application.objects.execute(TPostReply.select(TPostReply,TUser.nick_name,TUser.avatar).join(TUser,on=(TPostReply.reply_user_id==TUser.id)).where(TPostReply.post_id==post,TPostReply.reply_parent_id==None).order_by(TPostReply.cr_date.asc()))
            re_data['post_id']=post_id
            for comment in reply_list:
                commentList.append({
                    "id":comment.id,
                    "content":comment.content,
                    "comment_user_id":comment.reply_user_id,
                    "comment_user_name":comment.tuser.nick_name,
                    "comment_user_avatar":comment.tuser.avatar,
                    "add_time":comment.cr_date.strftime("%Y-%m-%d %H:%M:%S"),
                })
            re_data['commentList']=commentList
        except TPost.DoesNotExist as e:
            self.set_status(400)
            re_data['post_id']='post_id不存在'
        self.finish(json.dumps(re_data))

    #新增评论
    @authenticated_async
    async def post(self,post_id, *args, **kwargs):
        re_data = {}
        remote_ip = self.request.remote_ip
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)
        except json.decoder.JSONDecodeError as e:
            param = None
        comment_form = commentForm.from_json(param)
        if comment_form.validate():
            # 是个list
            content = comment_form.content.data
            ip = remote_ip
            cr_user_id = self.current_user.id
            reply_user_name=self.current_user.nick_name

            try:
                post = await self.application.objects.get(TPost, id=int(post_id))

                post_reply = await self.application.objects.create(TPostReply, post_id=post_id,target_user_id=post.cr_user_id, content=content, ip=ip,reply_user_id=cr_user_id,reply_user_name=reply_user_name,is_read=0, cr_date=datetime.datetime.now(),op_date=datetime.datetime.now())


                await self.application.objects.execute(TPost.update(reply_count=post.reply_count+1,last_reply_user_id=cr_user_id,last_reply_time=datetime.datetime.now()).where(TPost.id == int(post.id)))
                re_data['post_id']=post.id
                re_data['reply_user_id']=post_reply.reply_user_id
                re_data['msg']='success'
            except DoesNotExist as e:
                self.set_status(400)
                re_data['post_id']='帖子id不存在'


        else:
            self.set_status(400)
            for feild in comment_form.errors:
                re_data[feild] = comment_form.errors[feild][0]

        self.finish(json.dumps(re_data, default=json_serial))



class comment_reply(BaseHandler):

    @authenticated_async
    async def get(self,comment_id, *args, **kwargs):
        re_data = {}
        replytList = []
        try:
            reply_comment = await self.application.objects.get(TPostReply,id=int(comment_id))

            reply_list = await self.application.objects.execute(
                TPostReply.select().where(TPostReply.reply_parent_id == int(comment_id)).order_by(
                    TPostReply.cr_date.asc()))
            re_data['comment_id'] = int(comment_id)
            for reply in reply_list:
                replytList.append({
                    "id": reply.id,
                    "content": reply.content,
                    "comment_user_id": reply.reply_user_id,
                    "comment_user_name": reply.reply_user_name,
                    "add_time": reply.cr_date.strftime("%Y-%m-%d %H:%M:%S"),
                })
            re_data['replyList'] = replytList
        except TPostReply.DoesNotExist as e:
            self.set_status(404)
            re_data['comment_id'] = '评论id不存在'
        self.finish(json.dumps(re_data))



    @authenticated_async
    async def post(self,comment_id, *args, **kwargs):
        re_data = {}
        remote_ip = self.request.remote_ip
        try:
            param = self.request.body.decode("utf-8")
            param = json.loads(param)
        except json.decoder.JSONDecodeError as e:
            param = None
        reply_form = replyForm.from_json(param)
        if reply_form.validate():
            content=reply_form.content.data
            post_id=reply_form.post_id.data
            ip = remote_ip
            cr_user_id = self.current_user.id
            reply_user_name = self.current_user.nick_name
            comment_id=int(comment_id)

            try:
                post = await self.application.objects.get(TPost, id=int(post_id))
                comment_reply=await self.application.objects.get(TPostReply,id=int(comment_id))
                await self.application.objects.create(TPostReply, post_id=post_id,target_user_id=comment_reply.reply_user_id, content=content, ip=ip,reply_parent_id=comment_id,reply_user_id=cr_user_id,reply_user_name=reply_user_name,is_read=0, cr_date=datetime.datetime.now(),op_date=datetime.datetime.now())
                post.reply_count+=1

                await self.application.objects.update(post)

            except TPost.DoesNotExist as e:
                re_data['post_id']='帖子id不存在！'
                self.set_status(404)
            except TPostReply.DoesNotExist as e:
                re_data['comment_id'] = '评论id不存在！'
                self.set_status(404)


            self.finish(re_data)


class notice(BaseHandler):
    @authenticated_async
    async def get(self, *args, **kwargs):
        re_data={}
        data=[]
        user_id=self.current_user.id

        post_replys=await self.application.objects.execute(
            TPostReply.select().where((TPostReply.target_user_id==user_id)&(TPostReply.reply_user_id!=user_id)&(TPostReply.is_read==0))
        )
        count=0
        for reply in post_replys:
            count+=1
            time_day=(datetime.datetime.now() - reply.cr_date).days
            time_hour=(datetime.datetime.now() - reply.cr_date).seconds//3600
            if time_day==0:
                time_str=str(time_hour)+'小时前'
            else:
                time_str=str(time_day)+'天前'
            data.append(
                {'id':reply.id,
                 'post_id':reply.post_id,
                 'user_id':reply.reply_user_id,
                 'user_name':reply.reply_user_name,
                 'date':time_str,
                 'content':reply.content
                 })
        re_data["data"]=data
        re_data["total"]=count
        self.finish(re_data)
