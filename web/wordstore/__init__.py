# -*- coding: utf-8 -*-
from flask import Flask, session
from flask.ext.cache import Cache
from flask.ext.themes import setup_themes
from flask.ext.mongokit import MongoKit
from application import register_views, register_filters, register_db, set_logging, \
    configure_errorhandlers, configure_develop_handlers
import config

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY
app.config['CACHE_TYPE'] = config.CACHE_TYPE
app.config['MONGODB_HOST'] = config.MONGODB_HOST
app.config['MONGODB_PORT'] = config.MONGODB_PORT
app.config['MONGODB_DATABASE'] = config.MONGODB_DATABASE

db = MongoKit(app)
setup_themes(app, app_identifier='wordstore', theme_url_prefix='/themes')
cache = Cache(app)

register_db(db)
register_views(app)
register_filters(app)
configure_errorhandlers(app)

if config.DEV:
    configure_develop_handlers(app)

if not config.DEBUG:
    set_logging(app)
