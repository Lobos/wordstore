/**
 * User: Lobos841@gmail.com
 * Date: 2012-9-30
 */

(function () {
    window.WordStore = new Class({
        Implements: [Options, Events],

        options: {
            baseUrl: null
        },

        initialize: function (container, options) {
            this.container = document.id(container);
            this.setOptions(options);
            this.words = {};
        },

        loadWords: function (data) {
            data = data || [];
            data.each(function (d, index) {
                var word = this.words[d.id] = new Word(this.container, {
                    data: d,
                    onNext: function (el) {
                        this.start(el.getNext());
                    }.bind(this),
                    onFinish: function (pass) {
                        this.fireEvent('finish', [d.id, pass]);
                    }.bind(this)
                });
                if (index == 0)
                    this.start(word.stage);
            }.bind(this));
        },

        start: function (el) {
            if (el) {
                var id = el.retrieve('id');
                this.words[id].show();
            } else {
                this.fireEvent('over');
            }
        }

    });

    var Word = new Class({
        Implements: [Options, Events],

        options: {},

        initialize: function (container, options) {
            this.setOptions(options);
            this.container = container;
            this.createStage1(options.data);
            this.score = 0;
        },

        createStage1: function (data) {
            var self = this;
            var dl = this.stage = new Element('dl').store('id', data.id).inject(this.container);

            var dt = new Element('dt', {
                'html': data.word
            }).inject(dl);

            if (data.sound) {
                this.audio = new Audio(data.sound);
                new Element('i', {
                    'class': 'icon-audio',
                    'events': {
                        'click': function () {
                            this.audio.play();
                        }.bind(this)
                    }
                }).inject(dt);
            }

            new Element('label', {'html': data.add_time}).inject(dt);
            new Element('label', {'html': data.sent}).inject(dt);

            var buttons = new Element('span', {'class':'right'}).inject(dt);
            [['Remember', 'success'], ['Forget', 'forget']].each(function (d) {
                new Element('button', {
                    'html': d[0],
                    'class': 'btn ' + d[1],
                    'type': 'button',
                    'events': {
                        'click': function () {
                            _showAnswer(d[0] == 'Remember');
                        }
                    }
                }).inject(buttons);
            });

            var dd = new Element('dd').inject(dl).slide('hide');
            new Element('p', {'html': '[' + data.phon + ']', 'class': 'phone'}).inject(dd);
            new Element('p', {'html': data.pos, 'class': 'pos' }).inject(dd);
            new Element('p', {'html': data.def }).inject(dd);
            if (data.sent)
                new Element('p', {'html': data.sent, 'class': 'sent' }).inject(dd);
            if (data.note)
                new Element('p', {'html': data.note }).inject(dd);

            var _showAnswer = function (remember) {
                dd.slide('in');
                buttons.empty();
                [['Right', 'success', 'remember'], ['Wrong', 'wrong', 'remember'], ['Next', 'wrong', 'forget']].each(function (d) {
                    new Element('button', {
                        'html': d[0],
                        'class': 'btn ' + d[1] + ' ' + d[2],
                        'type': 'button',
                        'events': {
                            'click': function () {
                                if (remember && d[0] == 'Right')
                                    self.score++;
                                _next();
                            }
                        }
                    }).inject(buttons);
                });
                buttons.getElements('.' + (remember ? 'forget' : 'remember')).hide();
            }.bind(this);

            var _next = function () {
                buttons.getChildren().set('disabled', 'disabled');
                this.createStage2(this.options.data);
                this.fireEvent('next', dl);
                dl.nix(true);
            }.bind(this);
        },

        createStage2: function (data) {
            var dl = this.stage = new Element('dl').store('id', data.id).inject(this.container);
            var dt = new Element('dt').inject(dl);

            var input_append = new Element('div', {'class': 'input-append'}).inject(dt);
            var text = new Element('input', {
                'type': 'text',
                'disabled': 'disabled',
                'events': {
                    'keyup': function (event) {
                        if (event.key == 'enter')
                            _checkText();
                    }
                }
            }).inject(input_append);
            new Element('button', {
                'html': 'ok',
                'type': 'button',
                'disabled': 'disabled',
                'class':'btn',
                'events': {
                    'click': function () {
                        _checkText();
                    }
                }
            }).inject(input_append);
            var wrong = new Element('span', {
                'class': 'label label-warning',
                'html': 'Wrong, try again.'
            }).fade('hide').inject(input_append, 'after');

            new Element('label', {'html': data.def}).inject(dt);

            var dd = new Element('dd').inject(dl).slide('hide');
            new Element('h3', {'html': data.word }).inject(dd);
            new Element('p', {'html': '[' + data.phon + ']<i class="icon-audio"></i>', 'class': 'phone'}).inject(dd);
            new Element('p', {'html': data.pos, 'class': 'pos' }).inject(dd);
            new Element('p', {'html': data.def }).inject(dd);
            if (data.sent)
                new Element('p', {'html': data.sent, 'class': 'sent' }).inject(dd);
            if (data.note)
                new Element('p', {'html': data.note }).inject(dd);

            new Element('button', {
                'html': 'Next Word',
                'type': 'button',
                'class': 'btn right warning',
                'events': {
                    'click': function () {
                        this.set('disabled', 'disabled');
                        _next();
                    }
                }
            }).inject(dd);

            dd.getElement('.icon-audio').addEvent('click', function () {
                if (this.audio) this.audio.play();
            }.bind(this));

            var _counts = 0;
            var _checkText = function () {
                if (text.get('value').trim() == data.word) {
                    this.score++;
                    _next();
                    return;
                }

                if (_counts == 0) {
                    wrong.fade('in');
                } else {
                    wrong.fade('out');
                    input_append.getChildren().set('disabled', 'disabled');
                    dd.slide('in');
                }
                _counts++;
            }.bind(this);

            var _next = function () {
                this.fireEvent('finish', this.score >= 2);
                this.fireEvent('next', dl);
                dl.nix(true);
            }.bind(this);
        },

        show: function () {
            this.stage.addClass('active');
            this.stage.getElements(':disabled').removeProperty('disabled');
            if (this.audio) this.audio.play();
            var text = this.stage.getElement('input[type="text"]');
            if (text) text.focus();
        }

    });
})();