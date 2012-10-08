# -*- coding:utf-8 -*-

from flask import Blueprint, make_response
from ..helpers import user
from . import render_json
from utils import proxy

bp = Blueprint('api', __name__)

@bp.route('/api/iciba/<word>')
@user.require_login()
def iciba(word):
    url = 'http://dict-co.iciba.com/api/dictionary.php?w=' + word
    return get_xml(url)

@bp.route('/api/webster/<word>')
@user.require_login()
def webster(word):
    u = user.get_user()
    url = 'http://www.dictionaryapi.com/api/v1/references/learners/xml/%s?key=%s' % (word, u.webster_key)
    return get_xml(url)

def get_xml(url):
    resp = make_response(proxy(url).replace('\n', ''))
    resp.mimetype = 'text/xml'
    return resp

