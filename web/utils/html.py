# -*- coding: utf-8 -*-
import math, hashlib, urllib, urllib2, urlparse
import pymongo
from flask import request

def get_page_size(total=1, size=20):
    '''获取分页页码和条目数'''
    try:
        index = int(request.form.get('index'))
    except Exception:
        index = 1

    try:
        _size = int(request.form.get('size'))
        if _size > 0:
            size = _size
    except Exception:
        size = size

    if index * size > total + size:
        index = int(math.ceil(total/float(size)))

    if index < 1:
        index = 1

    skip = (index-1) * size

    return index, size, skip

def get_filters(*args):
    '''获取查询筛选条件'''
    filters = {}
    for k in args:
        if request.form.get(k):
            filters.update({ k: {'$regex' : request.form.get(k)} })
    return filters


def get_sort(default_key="_id", default_sort=pymongo.ASCENDING, allow_key=None):
    '''生成排序条件'''
    sort_key = request.form.get('sort[key]')
    sort_order = pymongo.DESCENDING if request.form.get('sort[order]') == "-1" else pymongo.ASCENDING
    if allow_key and sort_key in allow_key:
        return sort_key, sort_order
    elif allow_key is None and sort_key:
        return sort_key, sort_order
    else:
        return default_key, default_sort

def get_gravatar(email, size=48, avatar=None):
    from flask import url_for
    #default = request.url_root + 'static/images/avatar/default.png'
    if avatar:
        default = avatar
    else:
        default = url_for('static', filename='images/avatar/default.png')
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
    return gravatar_url

def get_avatar(id, email, size=48):
    return get_gravatar(email, size)

def proxy(url):
    #url 不能为unicode，要转为utf-8
    url = url.encode('utf-8')
    try:
        content = urllib2.urlopen(url, timeout=120).read()
        return content
    except:
        return u'error'
