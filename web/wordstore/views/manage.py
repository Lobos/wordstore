# -*- coding:utf-8 -*-
import datetime
from flask import Blueprint, redirect, url_for, jsonify, request, make_response
from utils import cn_time_now
from .. import db, app
from .. helpers import user
from . import is_login, render, render_json, render_success

bp = Blueprint('manage', __name__)

@bp.route('/manage/users')
@user.require_admin()
def users():
    pass

