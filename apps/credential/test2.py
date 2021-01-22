#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/4/12 10:22

import requests
import uuid



host='rngclub-1258903123.cos.ap-shanghai.myqcloud.com'

Length=561986
file_name=uuid.uuid1()

url='https://rngclub-1258903123.cos.ap-shanghai.myqcloud.com/avatar/{}.jpg'.format(file_name)

headers = {'Host': host, 'Content-Length': str(Length),'Content-Type':'multipart/form-data'}

with open(r'C:\Users\Public\Pictures\Sample Pictures\Lighthouse.jpg','rb') as f:
    file=f.read()


files={
    "key":'/avatar/{}.jpg'.format(file_name),
    "file":file
}

res=requests.post(url,headers=headers,files=files)
print(res.text)