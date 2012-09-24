# -*- coding:utf-8 -*-

from flask import Blueprint, redirect, url_for
from . import render

bp = Blueprint('account', __name__)

@bp.route('/account/login')
def login():
    return render('/account/login.html')

@bp.route('/account/logout')
def logout():
    return redirect(url_for('.login'))

@bp.route('/account/register')
def register():
    return render('/account/register.html')

@bp.route('/account/check_email')
def check_email():
    pass
