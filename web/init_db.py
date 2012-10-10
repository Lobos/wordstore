# -*- coding:utf-8 -*-

import datetime
from mongokit import Database, Connection
from wordstore.models import User
from config import DefaultConfig

def init_db():
    config = DefaultConfig()
    con = Connection(config.MONGODB_HOST, config.MONGODB_PORT)
    #con.drop_database(config.MONGODB_DATABASE)
    con.register(User)
    db = Database(con, config.MONGODB_DATABASE)

    index = 0
    for email in config.ADMIN:
        user = db.User()
        user['email'] = email
        user['password'] = db.User.encode_pwd(u'123456')
        user['create_time'] = datetime.datetime.now()
        user['nickname'] = u''
        if db.User.find({'email':email}).count() == 0:
            user.save()
            index += 1

    print '%s done.' % index

if __name__ == '__main__':
    init_db()