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
            data.each(function (d) {
                var word = this.words[d.id] = new Word(this.container, {
                    data: d,
                    onNext: function (el) {
                        this.start(el.getNext());
                    }.bind(this),
                    onDestroy: function () {
                        this.fireEvent(d.id);
                    }.bind(this)
                });
            }.bind(this));
            this.start();
        },

        start: function (el) {
            el = el || this.container.getFirst();
            var id = el.retrieve('id');
            this.words[id].show();
        },

        end: function () {
            this.fireEvent('end');
        }
    });

    var Word = new Class({
        Implements: [Options, Events],

        options: {},

        initialize: function (container, options) {
            this.setOptions(options);
            this.container = container;
            this.createStage1(options.data);
            this.createStage2(options.data);
            this.score = 0;
        },

        createStage1: function (data) {
            var self = this;
            var dl = this.stage = this.stage1 = new Element('dl').store('id', data.id).inject(this.container);

            var dt = new Element('dt', {
                'html': data.word
            }).inject(dl);

            if (data.pron) {
                this.audio = new Audio(data.pron);
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
            new Element('p', {'html': '<span class="ps">[' + data.ps + ']</span>'}).inject(dd);
            new Element('p', {'html': data.pos + ' ' + data.acceptation }).inject(dd);
            if (data.orig)
                new Element('p', {'html': data.orig + '<br />' + data.trans }).inject(dd);
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
                                    this.score++;
                                _next();
                            }
                        }
                    }).inject(buttons);
                });
                buttons.getElements('.' + (remember ? 'forget' : 'remember')).hide();
            }.bind(this);

            var _next = function () {
                this.fireEvent('next', dl);
                dl.nix(true);
                this.stage = this.stage2.inject(this.container);
            }.bind(this);
        },

        createStage2: function (data) {
            var dl = this.stage2 = new Element('dl').store('id', data.id);
            dl.set('html', 'stage2');
        },

        show: function () {
            this.stage.addClass('active');
        },

        destroy: function () {
            this.fireEvent('destroy');
        }
    });
})();