# -*- coding:utf-8 -*-
import codecs
import os, os.path

SCRIPTS_OUT = 'pack-script.js'
SCRIPTS_OUT_DEBUG = 'debug-script.js'
LAB_COMMON = '{common}'
LAB_LOCAL = '{local}'

JS_LIST = {
    'wordstore': [
        LAB_COMMON + 'mootools-core-1.4.5.js',
        LAB_COMMON + 'mootools-more-1.4.0.1.js',
        LAB_COMMON + 'mootools-exts.js',
        LAB_COMMON + 'form-validator.js',
        LAB_LOCAL + 'global.js',
    ]
}

def compress(app):
    common_path = 'static/js/'
    js_path = os.sep.join([app.root_path, 'static', 'js', ''])
    js_list = [f.replace(LAB_COMMON, common_path).replace(LAB_LOCAL, js_path) for f in JS_LIST[app.name]]
    script_debug = (js_path + SCRIPTS_OUT_DEBUG) if app.debug else '.temp'
    _execute(js_list, js_path + SCRIPTS_OUT, temp_file = script_debug)

def _execute(in_files, out_file, temp_file='.temp'):
    js_mtime = -1
    for f in in_files:
        mt = os.path.getmtime(f)
        if mt >= js_mtime:
            js_mtime = mt

    if not os.path.isfile(out_file):
        pack_mtime = -1
    elif temp_file != '.temp' and not os.path.isfile(temp_file):
        pack_mtime = -1
    else:
        pack_mtime = os.path.getmtime(out_file)

    if pack_mtime >= js_mtime:
        return

    print 'Compressing JavaScript...'
    temp = open(temp_file, 'w')
    for file_path in in_files:
        print file_path

        f = open(file_path, 'rb')
        header = f.read(4)

        # check if have BOM...
        bom_len = 0
        encodings = [(codecs.BOM_UTF32, 4),
                    (codecs.BOM_UTF16, 2),
                    (codecs.BOM_UTF8, 3)]

        # ... and remove appropriate number of bytes
        for h, l in encodings:
            if header.startswith(h):
                bom_len = l
                break
        f.seek(0)
        f.read(bom_len)

        content = f.read() + "\n"
        f.close()

        temp.write(content)

    temp.close()

    os.system('uglifyjs %s > %s' % (temp_file, out_file))

    org_size = os.path.getsize(temp_file)
    new_size = os.path.getsize(out_file)

    print '=> %s' % out_file
    print 'Original: %.2f kB' % (org_size / 1024.0)
    print 'Compressed: %.2f kB' % (new_size / 1024.0)
    print 'Reduction: %.1f%%' % (float(org_size - new_size) / org_size * 100)

    if temp_file == '.temp':
        os.remove(temp_file)
