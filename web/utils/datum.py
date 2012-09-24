# -*- coding: utf-8 -*-

from mongokit import Database, Connection
from utils import Ini
from models import Admin, AdminRole, Article
from datetime import datetime
from drone.helpers.menu import get_auth_list

ROOT_OBJECT_ID = '000000000000000000000001'

def init_test():
    config = Ini('config/common')
    db = config.DATABASE
    print init_db(db.MONGODB_HOST, db.MONGODB_PORT, db.TEST_DATABASE)

def init_db(host=None, port=None, database=None):
    con = Connection(host, port)
    con.drop_database(database)
    con.register([Admin, AdminRole])
    db = Database(con, database)

    generate_index(host, port, database)

    role = db.AdminRole()
    role['name'] = u'管理员'
    role['auth_list'] = get_auth_list()
    role.save()

    user = db.Admin()
    user['email'] = u'admin@test.com'
    user['name'] = u'admin'
    user['password'] = db.Admin.encode_pwd('123456')
    user['login_time'] = datetime.now()
    user['status'] = True
    user['role'] = role
    user.save()

    return 'success'

def generate_index(host=None, port=None, database=None):
    con = Connection(host, port)
    con.register([Article])
    db = Database(con, database)

    db.Article.generate_index(db.article)
