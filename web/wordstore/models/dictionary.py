# -*- coding:utf-8 -*-

from flaskext.mongokit import Document

class Dictionary(Document):
    __collection__ = 'dictionary'
    structure = {
        'word': unicode,
        'inflections': [unicode],
        'phon': unicode,
        'sound': unicode,
        'def': unicode
    }

    required_fields = ['word']
    indexes = [{
        'fields': 'word', 'unique': True
    }]
    default_values = { 'inflections': [] }

