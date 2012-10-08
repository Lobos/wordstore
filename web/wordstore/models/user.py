# -*- coding:utf-8 -*-
from datetime import datetime
from flask import request
from flaskext.mongokit import Document
from mongokit import DocumentMigration
from utils import md5, cn_time_now
from . import max_length

class UserMigration(DocumentMigration):
    def migration01__add_webster_key(self):
        self.target = {'webster_key':{'$exists':False}}
        self.update = {'$set':{'webster_key':u''}}

    def migration02__remove_words(self):
        self.target = {'words':{'$exists':True}}
        self.update = {'$unset':{'words':[]}}

class User(Document):
    __collection__ = 'user'
    structure = {
        'nickname': unicode,
        'email': unicode,
        'password': unicode,
        'login_ip': unicode,
        'login_time': datetime,
        'create_time': datetime,
        'webster_key': unicode
    }

    use_autorefs = True
    required_fields = ['password', 'email']
    validators = {
        'nickname': max_length(18)
    }
    indexes = [{
        'fields': 'email', 'unique': True
    }]
    migration_handler = UserMigration

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

class UserInfo(object):
    def __init__(self, **args):
        self.id = args.get('id')
        self.nickname = args.get('nickname', '')
        self.email = args.get('email')
        self.webster_key = args.get('webster_key', '')
        self.count = args.get('count', 0)