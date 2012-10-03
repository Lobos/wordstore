# -*- coding:utf-8 -*-
import base64
from functools import wraps
from flask import session, request, redirect, url_for, jsonify, abort
from ..models import UserInfo
from utils import pydes, json
from .. import db, config
import cache

SESSION_USER = 'user'
COOKIE_USER = '_wsid'

# login =============================================================
def login(email, password):
    if not email or not password:
        return None
    model = db.User.login(email, password)
    if model:
        user_data = UserInfo(model['_id'], model['nickname'], model['email'], model.word_count())
        session[SESSION_USER] = user_data
        return user_data
    else:
        return None

def get_user():
    if SESSION_USER in session:
        return session[SESSION_USER]
    else:
        email, password = cookie_decode(request.cookies.get(COOKIE_USER))
        return login(email, password)

def get_user_model():
    u = get_user()
    if u is None:
        return None

    return db.User.get_from_id(u.id)

def clear_session():
    session.pop(SESSION_USER, None)

# cookie code ======================================================
def cookie_encode(name, pwd):
    dd = { 'email': name, 'pwd': pwd }
    ds = json.dumps(dd)
    return _encode(ds)

def cookie_decode(str):
    if str is None:
        return None, None
    try:
        ds = _decode(str)
        dd = json.loads(ds)
        return dd['email'], dd['pwd']
    except Exception:
        return None, None

def _get_des():
    return pydes.des('DESCRYPT', pydes.CBC, config.DES_KEY, padmode=pydes.PAD_PKCS5)

def _encode(str):
    des = _get_des()
    return base64.b64encode(des.encrypt(str))

def _decode(str):
    des = _get_des()
    return des.decrypt(base64.b64decode(str), padmode=pydes.PAD_PKCS5)

# check ============================================================
def require_login(json=False):
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):
            user = get_user()

            if user is None:
                if json:
                    return jsonify(status=0, msg=u'请先登录')
                return redirect(url_for('account.login') + '?next=' + request.path)

            return f(*args, **kwargs)
        return func
    return decorator

def require_admin():
    def decorator(f):
        @wraps(f)
        def func(*args, **kwargs):
            user = get_user()

            if user is None or user.email not in config.ADMIN:
                abort(404)

            return f(*args, **kwargs)
        return func
    return decorator

def check_invitation(code, remove=False):
    lst = cache.get_invitation_codes()
    suc = code in lst
    if suc and remove:
        remove_invitation(code)
    return suc

def remove_invitation(code):
    db.invitation.remove({'code': code})
    cache.clear_invitation()

