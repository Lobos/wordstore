# -*- coding:utf-8 -*-
import os
import subprocess

def lesscss(app):
    paths = [
        '/static',
        '/themes'
    ]
    less_paths = []
    for p in paths:
        folder_path = app.root_path + p
        for path, subdirs, filenames in os.walk(folder_path):
            less_paths.extend([
                os.path.join(path, f)
                for f in filenames if f == 'pack.less'
            ])

    for less_path in less_paths:
        _create_css(less_path)

def _create_css(less_path):
    less_mtime = os.path.getmtime(less_path)

    less_paths = []
    for path, subdirs, filenames in os.walk(os.path.dirname(less_path)):
        less_paths.extend([
            os.path.join(path, f)
            for f in filenames if os.path.splitext(f)[1] == '.less'
        ])

    for lp in less_paths:
        mt = os.path.getmtime(lp)
        if mt >= less_mtime:
            less_mtime = mt

    css_folder = os.path.dirname(less_path)
    css_path = os.path.join(css_folder, 'pack.css')
    if not os.path.isfile(css_path):
        css_mtime = -1
    else:
        css_mtime = os.path.getmtime(css_path)

    if less_mtime >= css_mtime:
        subprocess.call(['node', 'tools/less/bin/lessc', less_path, css_path, '-x'], shell=False)

