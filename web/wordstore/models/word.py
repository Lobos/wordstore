# -*- coding:utf-8 -*-
from datetime import datetime
from flaskext.mongokit import Document
from . import ObjectId

class Word(Document):
    __collection__ = 'word'
    structure = {
        'user_id': ObjectId,
        'word': unicode,
        'sound': unicode,
        'phon': unicode,
        'pos': unicode,
        'def': unicode,
        'sent': unicode,
        'note': unicode,
        'add_time': datetime,
    }

    required_fields = ['word', 'user_id']
