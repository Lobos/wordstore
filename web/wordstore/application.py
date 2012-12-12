# -*- coding:utf-8 -*-
from flask import request, jsonify, redirect, url_for

def register_db(db):
    from models import User, Invitation, Word, Dictionary
    db.register([User, Invitation, Word, Dictionary])

def register_views(app):
    from views import home, account, word, manage, api
    app.register_blueprint(home.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(word.bp)
    app.register_blueprint(manage.bp)
    app.register_blueprint(api.bp)

def register_filters(app):
    from utils import filters, string, format_datetime
    app.jinja_env.filters['format_datetime'] = format_datetime
    app.jinja_env.filters['ids'] = filters.ids
    app.jinja_env.filters['json'] = filters.json_encode
    app.jinja_env.filters['tbr'] = filters.to_br
    app.jinja_env.filters['fmt_checked'] = filters.fmt_checked
    app.jinja_env.filters['markdown'] = string.markdown
    app.jinja_env.filters['truncate'] = string.truncate
    app.jinja_env.filters['get_ext'] = string.get_ext

    from utils import get_uid, get_gravatar, get_avatar, tree_root_id
    app.jinja_env.globals['get_uid'] = get_uid
    app.jinja_env.globals['gravatar'] = get_gravatar
    app.jinja_env.globals['get_avatar'] = get_avatar
    app.jinja_env.globals['tree_root_id'] = tree_root_id

    from helpers import get_user, main_script_url
    app.jinja_env.globals['main_script_url'] = main_script_url
    app.jinja_env.globals['get_user'] = get_user

def configure_develop_handlers(app):
    from flaskext.assets import set_less_handlers, set_js_handlers
    set_less_handlers(app)

    from helpers import get_script_list
    set_js_handlers(app, get_script_list())

def configure_errorhandlers(app):
    from views import render, render_json

    if app.testing:
        return

    @app.errorhandler(404)
    def page_not_found(error):
        if request.is_xhr:
            return render_json(u'查看的内容不存在')
        return render("errors/404.html", error=error)

    @app.errorhandler(403)
    def forbidden(error):
        if request.is_xhr:
            return render_json(u'Sorry, not allowed')
        return render("errors/403.html", error=error)

    @app.errorhandler(500)
    def server_error(error):
        if request.is_xhr:
            return render_json(u'出错了...')
        return render("errors/500.html", error=error)

    @app.errorhandler(401)
    def unauthorized(error):
        if request.is_xhr:
            return render_json(u"要登录的")
        return redirect(url_for("account_login.login", next=request.path))

def set_logging(app):
    import os, logging, codecs
    from logging import FileHandler
    from logging import Formatter
    from datetime import datetime

    file_name = '%s/log/%s.log' % (app.root_path, datetime.now().strftime('%Y%m%d'))
    if not os.path.exists(file_name):
        f = codecs.open(file_name, "w", "utf-8")
        f.close()

    file_handler = FileHandler(file_name)
    file_handler.setLevel(logging.WARNING)

    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(file_handler)
