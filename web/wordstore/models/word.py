# -*- coding:utf-8 -*-
from datetime import datetime
from flaskext.mongokit import Document
from . import ObjectId

class Word(Document):
    __collection__ = 'word'
    structure = {
        'word': unicode,
        'user_id': ObjectId,
        'add_time': datetime
    }