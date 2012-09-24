# -*- coding:utf-8 -*-

from . import json
import general, tree

def to_str(value):
    return str(value)

def http_fix(url):
    if url:
        if url.find('http'):
            url = 'http://%s' % url
    return url

def to_br(value):
    """\n转为<br /> 只允许换行"""
    return value.replace('\n', '<br />')

def ids(value):
    return [str(m['_id']) for m in value]

def json_encode(data):
    return json.dumps(data)

def fmt_checked(val):
    str = ''
    if val is True:
       str = 'checked'
    return str
