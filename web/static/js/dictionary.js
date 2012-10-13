/**
 * User: Lobos841@gmail.com
 * Date: 2012-9-27
 */

(function () {
    window.Dictionary = new Class({
        Implements: [Options, Events],

        options: {
            saveUrl: null,
            timeOut: 180 * 1000,
            api: []
        },

        initialize: function (container, options) {
            this.setOptions(options);
            this.container = document.id(container);
            this.words = [];
            this.current = null;
            this.next = null;
        },

        addWords: function (words) {
            var self = this;
            words = typeOf(words) == 'string' ? [words] : words;
            words.each(function (w) {
                var options = Object.merge(Object.clone(self.options), {
                    onComplete: function () {
                        self.show();
                    }
                });
                var word = new _Word(w.trim(), options);
                word.element.inject(this.container);
                this.words.push(word);
            }.bind(this));
            return this;
        },

        show: function () {
            this.current = this.words.shift();
            if (this.current) {
                this.current.load().show();
                this.loadNext();
            } else {
                this.fireEvent('complete');
            }
        },

        loadNext: function () {
            var word = this.words[0];
            if (word) word.load();
        }

    });

    var _Word = new Class({
        Implements: [Events, Options],

        options: {
            saveUrl: null,
            api: []
        },

        initialize: function (word, options) {
            this.word = word;
            this.setOptions(options);
            this.createElement();
            this.times = 0;
        },

        createElement: function () {
            var dl = this.element = new Element('dl');

            this.head = new Element('dt', {
                'html': this.word + '<i class="load"></i>'
            }).inject(dl);

            this.body = new Element('dd').inject(dl);
        },

        show: function () {
            this.element.addClass('active');
            new Fx.Scroll(window).toTop();
            return this;
        },

        load: function () {
            this.head.getElement('.load').addClass('show');
            this.body.empty();
            this.getApi().load();
            return this;
        },

        getApi: function () {
            var a = this.options.api[this.times % this.options.api.length],
                url = a.url.substitute({word:this.word}),
                api,
                options = {
                    onComplete: function (json) {
                        this.head.getElement('.load').removeClass('show');
                        if (json.status == 1)
                            this.createBody(json);
                        else
                            this.createError(json);
                    }.bind(this)
                };

            switch (a.id) {
                case 'webster':
                    api = _Api.Webster;
                    break;
                case 'dict':
                    api = _Api.Dict;
                    break;
            }
            return new api(url, options);
        },

        close: function () {
            this.element.nix(true);
            this.fireEvent('complete');
        },

        createBody: function (json) {
            this.data = json;
            var dd = this.body;
            new Element('h3', {
                'html': json.word
            }).inject(dd);

            var ps = new Element('p', {'html': '<span class="phon">[' + json.phon + ']</span>'}).inject(dd);
            if (json.sound) {
                var audio = this.audio = new Audio(json.sound);
                new Element('i', {
                    'class': 'icon-audio',
                    'events': {
                        'click': function () {
                            audio.play();
                        }
                    }
                }).inject(ps);
            }
            json.elements.inject(dd);

            var _checked = 'checked';
            dd.getElements('.sent, .def').addEvent('click', function () {
                dd.getElements('.' + _checked).removeClass(_checked);
                this.addClass(_checked);
                if (this.hasClass('sent')) {
                    this.getParent('p').getElement('.def').addClass(_checked);
                } else {
                    var next = this.getNext('span');
                    if (next && next.hasClass('sent'))
                        next.addClass(_checked);
                }
                var pos = this.getPrevious('.pos');
                if (!pos) pos = this.getParent('p').getPrevious('p span.pos');
                if (pos) pos.addClass(_checked);
            });
            dd.getElements('.pos').addEvent('click', function () {
                dd.getElements('.pos').removeClass(_checked);
                this.addClass(_checked);
            });

            new Element('textarea', {
                'class': 'span6',
                'name': 'note',
                'rows': 3
            }).inject(dd);

            this.alertHandle = new Element('p', {
                'class': 'alert alert-error'
            }).inject(dd);
            this.alertHandle.dissolve();

            var p = new Element('p').inject(dd);
            this.createButtons(1, p);
        },

        createError: function (json) {
            this.alert(json.msg);
            this.createButtons(json.status, this.body);
        },

        alert: function (msg) {
            var _alert = document.id(this.alertHandle);
            if (!_alert) {
                _alert = new Element('label', {
                    'html': msg,
                    'class': 'alert alert-error'
                }).inject(this.body);
            } else {
                _alert.set('html', msg);
            }

            _alert.reveal();
        },

        save: function () {
            var _get = function (name) {
                var el = this.body.getElement('span.' + name + '.checked');
                return el ? el.get('html') : '';
            }.bind(this);
            var data = {
                word: this.data.word,
                phon: this.data.phon,
                sound: this.data.sound,
                pos: _get('pos'),
                def: _get('def'),
                sent: _get('sent'),
                note: this.body.getElement('textarea').get('value')
            };
            new Request.JSON({
                url: this.options.saveUrl,
                data: data,
                onSuccess: function (json) {
                    if (json.status == 1) {
                        this.close();
                    } else {
                        this.body.getElements('button').removeProperty('disabled');
                        this.alert(json.msg);
                    }
                }.bind(this)
            }).send();
        },

        createButtons: function (status, wrapper) {
            var self = this;
            var dis = function () {
                wrapper.getElements('button').set('disabled', 'disabled');
            };
            if (status == 1) {
                new Element('button', {
                    'html': 'Submit',
                    'type': 'button',
                    'class': 'btn success',
                    'events': {
                        'click': function () {
                            dis();
                            self.save();
                        }
                    }
                }).inject(wrapper);
                /*new Element('button', {
                    'html': 'Reset',
                    'type': 'button',
                    'class': 'btn',
                    'events': {
                        'click': function () {
                            self.body.getElements('input[type="radio"]').removeProperty('checked');
                        }
                    }
                }).inject(wrapper);*/
            }

            new Element('button', {
                'html': 'Retry',
                'type': 'button',
                'class': 'btn warning',
                'events': {
                    'click': function () {
                        dis();
                        self.load();
                    }
                }
            }).inject(wrapper);

            new Element('button', {
                'html': 'Drop',
                'type': 'button',
                'class': 'btn remove',
                'events': {
                    'click': function () {
                        dis();
                        self.close();
                    }
                }
            }).inject(wrapper);
        }
    });

    var _Api = new Class({
        Implements: [Events, Options],

        options: {},

        initialize: function (url, options) {
            this.url = url;
            this.setOptions(options);
        },

        getRequest: function () {
            return new Request({
                url: this.url,
                method: 'get',
                onSuccess: function (text, xml) {
                    this.parse(xml);
                }.bind(this),
                onFailure: function () {
                    this.fireEvent('complete', {status:0});
                }.bind(this)
            });
        },

        parse: function () {
            //pass
        },

        load: function () {
            this.getRequest().send();
        }
    });

    _Api.Dict = new Class({
        Implements: [_Api],

        getRequest: function () {
            return new Request.JSON({
                url: this.url,
                method: 'get',
                onSuccess: function (json) {
                    if (json.status == 0)
                        this.fireEvent('complete', json);
                    else
                        this.parse(json);
                }.bind(this),
                onFailure: function () {
                    this.fireEvent('complete', {status:0, msg:'error'});
                }.bind(this)
            });
        },

        parse: function (json) {
            var el = new Element('div');
            var ig = /^\s+\d.*(:$|----------\/\/$|]\/\/$)/;

            var _sent = function (line, i) {
                var arr = [];
                if (line.trim().length == 0) return arr;
                var index = line.indexOf('  --');
                var pos = i === 0 ? 'pos' : 'def';
                if (pos == 'def') {
                    var re = new RegExp('^\\s?' + json.word + '\\s+\\d');
                    if (re.test(line)) pos = 'pos';
                }

                if (index < 0) {
                    arr.push('<span class="{0}">{1}</span>'.format(pos, line));
                } else if (index == 0) {
                    line = line.replace('  --', '');
                    index = line.indexOf('  --');
                    arr.push('<span class="sent">--{0}</span>'.format(index < 0 ? line: line.substring(0, index)));
                    if (index > 0) arr.append(_sent(line.substring(index)));
                } else {
                    arr.push('<span class="{0}">{1}</span>'.format(pos, line.substring(0, index)));
                    arr.append(_sent(line.substring(index)));
                }
                return arr;
            };

            json.def.split('\\n').each(function (t, i) {
                if (ig.test(t)) return;
                t = t.replace('----------//', '');
                if (t.test(/\/\//))
                    t = t.substring(0, t.length - 2);

                var newt = [];
                t.split('//').each(function (line, j) {
                    newt.append(_sent(line, i+j));
                });

                new Element('p', { html: newt.join('<br />') }).inject(el);
            });

            json.elements = el.getChildren();
            this.fireEvent('complete', json);
        }
    });

    _Api.Webster = new Class({
        Implements: [_Api],

        parse: function (xml) {
            var doc = xml.documentElement;
            var dict = {
                status: 1,
                words: []
            };
            doc.getElements('entry').each(function (entry) {
                var word = {
                    word: entry.get('id')
                };
                dict.words.push(word);
            });
            
            this.fireEvent('complete', dict);
        }
    });
})();