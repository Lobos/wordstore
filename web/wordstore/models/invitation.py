# -*- coding:utf-8 -*-

import random
from flaskext.mongokit import Document
from utils import radix_str

class Invitation(Document):
    __collection__ = 'invitation'
    structure = {
        'code': unicode
    }

    def create_code(self):
        long_code = random.randint(10000000000000000000, 99999999999999999990)
        code = radix_str(long_code, 36)
        self['code'] = code
