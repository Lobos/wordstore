# -*- coding:utf-8 -*-

from flask import Blueprint, request, make_response
from utils import proxy
from .. import db, app
from .. helpers import user
from . import render, render_json, render_success

bp = Blueprint('word', __name__)

@bp.route('/word/index')
@user.require_login()
def index():
    pass

@bp.route('/word/add', methods=['GET', 'POST'])
@user.require_login()
def add():
    return render('word/add.html')

@bp.route('/word/iciba/')
@bp.route('/word/iciba/<word>')
@user.require_login()
def iciba(word = None):
    if not word:
        return render_json('')
    url = 'http://dict-co.iciba.com/api/dictionary.php?w=' + word
    resp = make_response(proxy(url).replace('\n', ''))
    resp.mimetype = 'text/xml'
    return resp

