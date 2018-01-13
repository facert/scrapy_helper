# -*- coding: utf-8 -*-

from random import Random
from hashlib import md5
from django.conf import settings


# 获取由4位随机大小写字母、数字组成的salt值
def create_salt(length=4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in xrange(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt


def create_md5():
    salt = create_salt()
    md5_obj = md5()
    md5_obj.update(salt)
    return md5_obj.hexdigest()
