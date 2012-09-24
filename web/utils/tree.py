# -*- coding:utf-8 -*-
from utils import json

ROOT_OBJECT_ID = '000000000000000000000001'
class Tree(object):
    def __init__(self, id, pid, name, index=0, type='folder'):
        self.property = {
            'id': id,
            'name': name
        }
        self.id = id
        self.pid = pid
        self.children = []
        self.type = type
        self.index = index

def encode_tree(obj):
    if not isinstance(obj, Tree):
        raise TypeError("%r is not JSON serializable" % (obj,))
    return obj.__dict__

def refactor(lst, root_pid):
    d = dict()
    for t in lst:
        d[t.id] = t

    l = list()
    for t in lst:
        if not t.pid or (t.pid == root_pid):
            l.append(t)
        elif d.has_key(t.pid):
            d[t.pid].children.append(t)

    sort(l)
    return l

def sort(lst):
    lst.sort(key=lambda t:t.index, reverse=True)
    for t in lst:
        sort(t.children)

def dumps(lst, root_pid=ROOT_OBJECT_ID, add_root=True):
    l = refactor(lst, root_pid)
    root = []
    if add_root:
        r = Tree(ROOT_OBJECT_ID, '', 'root')
        r.children = l
        root.append(r)
    else:
        root = l
    return json.dumps({'status':1, 'data':root}, default=encode_tree)

def tree_root_id():
    return tree.ROOT_OBJECT_ID


