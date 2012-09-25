# -*- coding:utf-8 -*-

from werkzeug.contrib.cache import SimpleCache
from .. import db

cache = SimpleCache()

# property ========================================================
_invitation_key = 'invitation_codes'
def get_invitation_codes():
    lst = cache.get(_invitation_key)
    if lst is None:
        lst = [m['code'] for m in db.Invitation.find()]
    return lst

def clear_invitation():
    cache.set(_invitation_key, None, timeout=1)

