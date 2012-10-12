# -*- coding:utf-8 -*-
import hashlib
from markdown import Markdown

def truncate(str, length, end='...'):
    """
    截取字符串，使得字符串长度等于length，并在字符串后加上省略号
    """
    is_encode = False
    try:
        str_encode = str.encode('gb18030') #为了中文和英文的长度一致（中文按长度2计算）
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                str = str_encode.decode('gb18030') + end
            except:
                str_encode = str_encode[:-1]
                try:
                    str = str_encode.decode('gb18030') + end
                except:
                    is_encode = False
    if not is_encode:
        if length < len(str):
            length = length - 2
            return str[:length] + '...'
    return str

def len_cn(str):
    """
    字符串长度，一个中文字符算2
    """
    try:
        str_encode = str.encode('gb18030')
        return len(str_encode)
    except:
        return len(str)

def strip_tags(text):
    """
    去除html标记
    """
    from HTMLParser import HTMLParser
    text = text.strip()
    text = text.strip('\n')
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(text)
    parse.close()
    return ''.join(result)

def md5(str):
    m = hashlib.md5()
    m.update(str)
    return unicode(m.hexdigest())

def markdown(str, safe_mode=False):
    md = Markdown(safe_mode=safe_mode)
    return md.convert(str)

def get_ext(str):
    if not str or ('.' not in str):
        return ''
    return str.rsplit('.', 1)[1]
