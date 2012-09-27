# -*- coding:utf-8 -*-
import urllib2
#try:
#    import xml.etree.cElementTree as ET
#except ImportError:
#    import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET

base_url = 'http://dict-co.iciba.com/api/dictionary.php?w='

def get_word(word):
    content = urllib2.urlopen(base_url + word).read().replace('\n', '')
    tree = ET.fromstring(content)

    dict = {
        'key': tree.find('key').text
    }

    return dict
