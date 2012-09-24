# -*- coding:utf-8 -*-
from datetime import datetime
from flask import request
from flaskext.mongokit import Document
from utils import md5, cn_time_now

class User(Document):
    __collection__ = 'admin'
    structure = {
        'name': unicode,
        'email': unicode,
        'password': unicode,
        'login_ip': unicode,
        'login_time': datetime
    }

    @staticmethod
    def encode_pwd(pwd):
        return md5(pwd)

    def login(self, email, password, encode_pwd=False):
        if encode_pwd:
            password = self.encode_pwd(password)

        model = self.find_one({ 'email': email, 'password': password })
        if model:
            model['login_ip'] = unicode(request.remote_addr)
            model['login_time'] = cn_time_now()
            model.save()
        return model

class UserInfo():
    def __init__(self, id, nickname, email, count):
        self.id = id
        self.nickname = nickname
        self.email = email
        self.count = count