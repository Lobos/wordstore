/**
 * User: Lobos841@gmail.com
 * Date: 2012-9-27
 */

(function () {
    window.Dictionary = new Class({
        Implements: [Options, Events],

        options: {
            saveUrl: null,
            api: {
                'iciba': 'http://dict-co.iciba.com/api/dictionary.php?w='
            }
        },

        initialize: function (container, options) {
            this.setOptions(options);
            this.container = document.id(container);
        },

        addWords: function (words) {
            words = typeOf(words) == 'string' ? [words] : words;
            words.each(function (w) {
                this.createSingle(w.trim());
            }.bind(this));
            return this;
        },

        createSingle: function (word) {
            var outer = new Element('dl', {
                'class': 'word'
            }).inject(this.container).store('word', word);

            var dt = new Element('dt', {
                'html': word + '<i class="load"></i>'
            }).inject(outer);

            new Element('dd').inject(outer);
        },

        getApi: function (times) {
            times = times || 0;
            var apis = this.options.api;
            var index = times % Object.getLength(apis);
            var key = Object.keys(apis)[index];
            return [key, apis[key]];
        },

        showFirst: function () {
            var first = this.container.getFirst();
            this.prepare(first).show(first);
            return this;
        },

        show: function (el) {
            if (!el) {
                this.fireEvent('complete');
                return this;
            }
            el.addClass('active');
            var next = el.getNext();
            if (next)
                this.prepare(next);
            return this;
        },

        prepare: function (el) {
            var word = el.retrieve('word');
            var times = el.retrieve('times') || 0;
            var api = this.getApi(times);
            this.createForm(el, api[0], api[1] + word);
            el.store('times', times+1);
            return this;
        },

        createForm: function (el, api, url) {
            var self = this;
            var _control = function (label, temp, data, form) {
                if (data.length == 0) return;
                var ct_str = ('<div class="control-group">' +
                    '<label class="control-label">{label}</label>' +
                    '<div class="controls"></div>' +
                    '</div>').substitute({label: label});
                var ct = Elements.from(ct_str)[0].inject(form);
                cc = ct.getElement('.controls');
                data.each(function (d, i) {
                    Object.merge(d, {
                        check: i == 0 ? 'checked="checked"' : ''
                    });
                    var item = Elements.from(temp.substitute(d))[0].inject(cc);
                    item.getElement('input').store('data', d);
                });
            };

            var _createButtons = function (status, wrapper) {
                if (status == 1) {
                    new Element('button', {
                        'html': '加入仓库',
                        'type': 'button',
                        'class': 'btn success',
                        'events': {
                            'click': function () {
                                self.saveWord(el);
                            }
                        }
                    }).inject(wrapper);
                    new Element('button', {
                        'html': '取消选择',
                        'type': 'button',
                        'class': 'btn warning',
                        'events': {
                            'click': function () {
                                el.getElements('input[type="radio"]').removeProperty('checked');
                            }
                        }
                    }).inject(wrapper);
                }

                new Element('button', {
                    'html': '重 试',
                    'type': 'button',
                    'class': 'btn warning',
                    'events': {
                        'click': function () {
                            self.prepare(el);
                        }
                    }
                }).inject(wrapper);

                new Element('button', {
                    'html': '放 弃',
                    'type': 'button',
                    'class': 'btn remove',
                    'events': {
                        'click': function () {
                            self.show(el.getNext());
                            el.nix(true);
                        }
                    }
                }).inject(wrapper);
            };

            var dd = el.getElement('dd').empty();
            var loading = el.getElement('dt > .load');
            loading.addClass('show');
            this.exec(api, url, function (dict) {
                loading.removeClass('show');
                var form = new Element('form', {
                    'class': 'form-horizontal'
                }).inject(dd);

                if (dict.status == 1) {
                    var temp = '<label class="radio"><input type="radio" name="ps" {check} /><span class="ps">[{ps}]</span>' +
                                '<i class="icon-audio"><audio><source src="{pron}" type="audio/mp3"></audio></i></label>';
                    _control('读音', temp, dict.ps, form);

                    temp = '<label class="radio"><input type="radio" name="pos" {check} />{pos} {acceptation}</label>';
                    _control('释义', temp, dict.pos, form);

                    temp = '<label class="radio"><input type="radio" name="sent" {check} />{orig}<br />{trans}</label>';
                    _control('例句', temp, dict.sent, form);

                    el.getElements('i.icon-audio').addEvent('click', function () {
                        this.getElement('audio').play();
                    });
                }

                var note = '<div class="control-group"><label class="control-label">笔记</label><div class="controls"><textarea rows="4" class="span6 note"></textarea></div></div>';
                Elements.from(note)[0].inject(form);

                var btn_container = new Element('div', {
                    'class': 'control-group'
                }).inject(form);
                _createButtons(dict.status, btn_container);
            });
        },

        saveWord: function (element) {
            var data = {
                word: element.retrieve('word'),
                note: element.getElement('.note').get('value')
            };
            element.getElements('input[type="radio"]:checked').each(function (el) {
                Object.merge(data, el.retrieve('data'));
            });

            if (this.options.saveUrl == null) return;
            new Request.JSON({
                url: this.options.saveUrl,
                data: data,
                onSuccess: function (json) {
                    if (json.status == 1) {
                        this.show(element.getNext());
                        element.nix(true);
                    } else {
                        alert(json.msg);
                    }
                }.bind(this),
                onFailure: function () {
                    alert('系统出错了..')
                }
            }).send();
        },

        exec: function (api, url, fn) {
            switch (api) {
                case 'iciba':
                    this.getIciba(url, fn);
                    break;
            }
        },

        getIciba: function(url, fn) {
            var _ps = function (doc, keys) {
                var lst = [];
                doc.getElements(keys[0]).each(function (el) {
                    var pp = {};
                    pp[keys[0]] = el.get('text');
                    if (keys[1]) pp[keys[1]] = el.getNext().get('text');
                    lst.push(pp);
                });
                return lst;
            };

            var parse = function (xml) {
                var doc = xml.documentElement;
                var dict = {
                    status: 1,
                    key: doc.getElement('key').get('text'),
                    ps: _ps(doc, ['ps', 'pron']),
                    pos: _ps(doc, ['pos', 'acceptation']),
                    sent: _ps(doc, ['orig', 'trans'])
                };
                return(dict);
            };

            new Request({
                url: url,
                onSuccess: function (text, xml) {
                    if (text == 'error') {
                        fn({ status: 0 });
                    } else {
                        var dict = parse(xml);
                        fn(dict);
                    }
                },
                onFailure: function () {
                    fn({ status: 0 });
                }
            }).get();
        }
    });
})();