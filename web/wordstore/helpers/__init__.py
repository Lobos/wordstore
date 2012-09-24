# -*- coding:utf-8 -*-
from flask import url_for
from .. import config
from user import get_user

def main_script_url():
    if config.DEBUG:
        script_name = 'debug-script.js'
    else:
        script_name = 'pack-script.js'

    return url_for('static', filename='js/' + script_name)