#!/user/bin/env.python
# _*_ coding;utf-8 _*_
# @Time     :2019/3/28 17:35
from random import choice

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