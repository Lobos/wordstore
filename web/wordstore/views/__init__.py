# -*- coding:utf-8 -*-
from flask import jsonify
from flaskext.themes import render_theme_template
from .. import config
from ..helpers.user import login, get_user, get_user_model, require_login

def render(template, **context):
    return render_theme_template(get_theme(), template, **context)

def render_json(msg, status=0, **kwargs):
    return jsonify(msg=msg, status=status, **kwargs)

def render_success(msg='', **kwargs):
    return render_json(msg, status=1, **kwargs)

def get_theme():
    return config.DEFAULT_THEME

# const ============================================================

HTML = 'html'
JSON = 'json'

def is_login():
    user = get_user()
    return user is not None