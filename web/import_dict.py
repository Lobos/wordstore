# -*- coding:utf-8 -*-
from mongokit import Database, Connection
from wordstore.models import Dictionary
from config import DefaultConfig

def import_dict():
    db = get_db()
    db.drop_collection(db.dictionary)
    db.Dictionary.generate_index(db.dictionary)

    index = 0
    f = open('../data/dict.txt', 'r')
    for line in f:
        w, _, d = line.partition('\t')
        word = db.Dictionary()
        word['word'] = unicode(w, errors='ignore')
        word['def'] = unicode(d, errors='ignore')
        word['inflections'] = [unicode(w, errors='ignore')]
        word['sound'] = get_sound(word['word'])
        word.save()
        print w
        index += 1

    print '%s done.' % index

def get_sound(word):
    if not word:
        return u''
    if not word[0].isalpha():
        return u''

    return u'/sound/%s/%s.ogg' % (word[0].upper(), word)

def import_inflections():
    db = get_db()
    f = open('../data/inflections.csv')
    for line in f:
        infs = [unicode(s, errors='ignore') for s in line.split(',') if len(s) > 1]
        if len(infs) > 1:
            word = db.Dictionary.find_one({'word':infs[0]})
            if word:
                word['inflections'] = infs
                word.save()
                print infs[0]

def import_phon():
    db = get_db()
    f = open('../data/phon.txt')
    for line in f:
        w, p = line.split('\t')
        print w, p
        word = db.Dictionary.find_one({'word':w})
        if word:
            word['phon'] = unicode(p.rstrip(), errors='ignore')
            word.save()

def get_db():
    config = DefaultConfig()
    con = Connection(config.MONGODB_HOST, config.MONGODB_PORT)
    con.register(Dictionary)
    db = Database(con, config.MONGODB_DATABASE)
    return db

if __name__ == '__main__':
    import_dict()
    import_inflections()
    import_phon()
