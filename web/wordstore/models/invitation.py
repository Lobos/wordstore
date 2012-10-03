# -*- coding:utf-8 -*-

import random, datetime
from flaskext.mongokit import Document
from utils import radix_str

class Invitation(Document):
    __collection__ = 'invitation'
    structure = {
        'code': unicode,
    }

    required_fields = ['code']

    def generate(self):
        long_code = random.randint(10000000000000000000, 99999999999999999990)
        code = unicode(radix_str(long_code, 36))
        self['code'] = code
