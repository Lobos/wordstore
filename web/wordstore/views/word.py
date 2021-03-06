# -*- coding:utf-8 -*-

from flask import Blueprint, request, make_response, abort, jsonify
from utils import proxy, cn_time_now
from .. import db, app
from .. models import ObjectId
from .. helpers import user
from . import render, render_json, render_success

bp = Blueprint('word', __name__)

@bp.route('/word/add', methods=['GET', 'POST'])
@user.require_login()
def add():
    if request.method == 'GET':
        return render('word/add.html')

    f = request.form
    model = db.Word()
    model['word'] = f.get('word')
    model['sound'] = f.get('sound')
    model['phon'] = f.get('phon')
    model['pos'] = f.get('pos')
    model['sent'] = f.get('sent')
    model['def'] = f.get('def')
    model['note'] = f.get('note')
    model['user_id'] = user.get_user().id
    model['add_time'] = cn_time_now()

    try:
        model.save()
        return render_success()
    except Exception, e:
        app.logger.error(e)
        return render_json(e)

@bp.route('/word/mine')
@user.require_login()
def mine():
    u = user.get_user()
    models = db.Word.find({ 'user_id': u.id }).sort('word')
    return render('word/mine.html', models = models)


@bp.route('/word/remove/', methods=['POST'])
@user.require_login()
def remove():
    try:
        id = ObjectId(request.form.get('id'))
        model = db.Word.get_from_id(id)
        u = user.get_user()
        if model and model['user_id'] == u.id:
            model.delete()
            return render_success()
        else:
            return render_json('')
    except Exception, e:
        abort(404)

@bp.route('/word/single/')
@bp.route('/word/single/<ObjectId:id>')
@user.require_login()
def single(id=None):
    model = db.Word.get_from_id(id)
    if model is None:
        abort(404)

    return render('word/_dd.html', model=model)

@bp.route('/word/finish/', methods=['POST'])
@user.require_login()
def finish():
    try:
        id = ObjectId(request.form.get('id'))
        pss = request.form.get('pass') == 'true'
        u = user.get_user()
        model = db.Word.find_one({ '_id':id, 'user_id': u.id })
        if not model:
            return render_json('')

        if pss:
            model.delete()
        else:
            model['add_time'] = cn_time_now()
            model.save()
        return render_success()
    except Exception, e:
        abort(404)
