# -*- coding:utf-8 -*-

from flask import Blueprint
from . import render
from .. helpers import user

bp = Blueprint('home', __name__)

@bp.route('/')
@user.require_login()
def index():
    return render('index.html')

