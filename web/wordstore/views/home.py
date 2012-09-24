# -*- coding:utf-8 -*-

from flask import Blueprint
from . import render

bp = Blueprint('home', __name__)

@bp.route('/')
def index():
    return render('index.html')

