# -*- coding:utf-8 -*-

from flask import Blueprint, request
from .. import db, app
from .. helpers import user, generate_get_word
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

@bp.route('/word/get/')
@bp.route('/word/get/<word>')
@user.require_login()
def get(word):
    if not word:
        return render_json('')
    data = generate_get_word()(word)
    return render('word/_dd.html', data = data)

