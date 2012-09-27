# -*- coding:utf-8 -*-
from datetime import datetime
from flaskext.mongokit import Document
from . import ObjectId

class Word(Document):
    __collection__ = 'word'
    structure = {
        'word': unicode,
        'user_id': ObjectId,
        'acceptation': unicode,
        'symbol': unicode,
        'pron': unicode,
        'sentence': unicode,
        'translate': unicode,
        'note': unicode,
        'add_time': datetime,
    }

    required_fields = ['word', 'user_id']
