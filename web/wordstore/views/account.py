# -*- coding:utf-8 -*-
import datetime
from flask import Blueprint, redirect, url_for, jsonify, request, make_response
from utils import cn_time_now
from .. import db, app
from .. helpers import user
from . import is_login, render, render_json, render_success

bp = Blueprint('account', __name__)

@bp.route('/account/login', methods=['GET', 'POST'])
def login():
    if is_login():
        return redirect(url_for('home.index'))

    if request.method == 'GET':
        return render('/account/login.html')

    f = request.form
    email = request.form.get('email')
    password = db.User.encode_pwd(f.get('password'))
    model = user.login(email, password)
    if model:
        resp = make_response(jsonify(status = 1))
        ds = user.cookie_encode(email, password)
        if request.form.get('remember') == 'on':
            expires = datetime.datetime.strptime('2037-01-01', '%Y-%m-%d')
            resp.set_cookie(user.COOKIE_USER, ds, expires=expires)
        else:
            resp.set_cookie(user.COOKIE_USER, ds)
        return resp

    else:
        return render_json(u'邮箱和密码不匹配...')


@bp.route('/account/logout')
def logout():
    user.clear_session()
    resp = make_response(redirect(url_for('.login')))
    expires = datetime.datetime.now() - datetime.timedelta(1)
    resp.set_cookie(user.COOKIE_USER, None, expires=expires)
    return resp

@bp.route('/account/register', methods=['GET', 'POST'])
def register():
    if is_login():
        return redirect(url_for('home.index'))

    if request.method == 'GET':
        return render('account/register.html')

    f = request.form
    if not user.check_invitation(f.get('invitation')):
        return render_json(u'邀请码不正确或者已被使用')

    model = db.User()
    model['email'] = f.get('email')
    exist = db.User.find({ 'email': model['email'] }).count() > 0
    if exist:
        return render_json(u'那个，邮箱%s已经存在...' % model['email'])

    model['create_time'] = cn_time_now()
    model['nickname'] = f.get('nickname')
    model['password'] = db.User.encode_pwd(f.get('password'))
    try:
        model.save()
        user.login(model['email'], model['password'])
        return render_success()
    except Exception, e:
        app.logger.error(e)
        return render_json(unicode(e))

@bp.route('/account/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    exist = db.User.find({ 'email': email }).count() > 0
    if exist:
        return render_json(u'邮箱已经存在了')
    else:
        return render_success()

@bp.route('/account/check_invitation', methods=['POST'])
def check_invitation():
    code = request.form.get('invitation')
    if not user.check_invitation(code):
        return render_json(u'邀请码不正确或者已被使用')
    else:
        return render_success()

@bp.route('/account/profile')
@user.require_login()
def profile():
    model = user.get_user_model()
    return render('account/profile.html', model=model)