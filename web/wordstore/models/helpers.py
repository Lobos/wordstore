# -*- coding:utf-8 -*-

from utils import len_cn

def max_length(length):
    def validate(value):
        if len_cn(value) <= length:
            return True
        raise Exception(u'%s最大字符长度不能超过' + str(length))
    return validate

def min_length(length):
    def validate(value):
        if len_cn(value) >= length:
            return True
        raise Exception(u'%s最少字符长度不能少于 %s' % length)
    return validate

