# -*- coding:utf-8 -*-

import datetime
from flask import Blueprint, jsonify
from utils import cn_time_now, format_datetime
from . import render
from .. import db, config
from .. helpers import user

bp = Blueprint('home', __name__)

@bp.route('/')
@user.require_login()
def index():
    return render('index.html')

@bp.route('/get_words')
@user.require_login()
def get_words():
    u = user.get_user()
    dt = cn_time_now() - datetime.timedelta(hours=config.BURY_HOURS)
    models = db.Word.find({ 'user_id': u.id, 'add_time': { '$lt': dt } })

    total = models.count()
    data = []
    keys = [ 'word', 'ps', 'pron', 'pos', 'acceptation', 'orig', 'trans', 'note' ]
    for m in models.limit(config.PAGE_SIZE):
        w = {
            'id': str(m['_id']),
            'add_time': format_datetime(m['add_time'])
        }
        for k in keys:
            w[k] = m[k]
        data.append(w)

    context = {
        'status': 1,
        'data': data,
        'total': total,
        'over': total <= config.PAGE_SIZE
    }
    return jsonify(context)