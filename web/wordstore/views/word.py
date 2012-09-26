# -*- coding:utf-8 -*-

from flask import Blueprint
from .. import db, app
from .. helpers import user
from . import render, render_json

bp = Blueprint('word', __name__)

@bp.route('/word/index')
@user.require_login()
def index():
    pass

@bp.route('/word/add', methods=['GET', 'POST'])
@user.require_login()
def add():
    return render('word/add.html')
