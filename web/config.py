# -*- coding:utf-8 -*-

class DefaultConfig(object):
    DEBUG = True
    DEV = True
    SECRET_KEY = "i*423^s~9l%Jd*2#"
    DES_KEY = "a2!D7=eE"
    DEFAULT_THEME = "default"
    SITE_NAME = u"wordstore"
    CACHE_TYPE = "simple"

    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017
    MONGODB_DATABASE = "wordstore"

    ADMIN = [u'admin@example.com']
    MAX_WORDS = 300
    BURY_HOURS = 8
    PAGE_SIZE = 10