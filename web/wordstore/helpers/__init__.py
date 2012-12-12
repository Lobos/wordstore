# -*- coding:utf-8 -*-
import os
from flask import url_for
from .. import app, config
from user import get_user

def main_script_url():
    if config.DEBUG:
        script_name = 'debug-script.js'
    else:
        script_name = 'pack-script.js'

    return url_for('static', filename='js/' + script_name)

def get_script_list():
    scripts = [
        'mootools-core-1.4.5.js',
        'mootools-more-1.4.0.1.js',
        'overlay.js',
        'mooui.js',
        'mooui-exts.js',
        'mooui-openbox.js',
        'mooui-select.js',
        'mooui-validator.js',
        'mooui-dropdown.js',
        'mooui-global.js'
    ]

    scripts = [ 'static/mooui-js/' + s for s in scripts ]

    locale_path = os.sep.join([app.root_path, 'static', 'js', ''])
    locale_scripts = [
        'dictionary.js',
        'wordstore.js',
        'global.js'
    ]
    for s in locale_scripts:
        scripts.append(locale_path + s)

    return scripts