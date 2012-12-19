(function () {
    window.$g = new new Class({
        append: function (objs) {
            Object.merge(this, objs);
        },

        initAlert: function (element) {
            this.topMessager = document.id(element).set('tween', {
                property: 'top',
                link: 'cancel'
            }).addEvent('click', function () {
                if (this.getStyle('top').toInt() >= -1)
                    this.tween(-1, -this.outerHeight());
            });
            if (this.topMessager.getElement('.alert').get('text'))
                this.alert(null, null, true);
        },

        initValidator: function (form, options) {
            options = Object.merge({
                successHtml: '<i class="icon-check"></i>'
            }, options);
            var formValidator = new MooUI.Validator(form, {
                evaluateOnBlur: false,
                onSuccess: function (el) {
                    var parent = el.getParent('.control-group');
                    parent.removeClass('error');
                    var help = parent.getElement('[class^=help-]');
                    if (help)
                        help.set('html', options.successHtml);
                },
                onFailure: function (el, msg) {
                    var parent = el.getParent('.control-group');
                    parent.addClass('error');
                    var help = parent.getElement('[class^=help-]');
                    if (help)
                        help.set('html', msg);
                }
            });
            return formValidator;
        },

        saveForm: function (options) {
            if (options.validator) {
                var suc = options.validator.validate();
                if (!suc) return false;
            }

            var rq = this.getRequest(options);
            var form = document.id(options.form);
            rq.send(form);
        },

        getRequest: function (options) {
            var self = this;
            if (options.button)
                options.button.set('disabled', 'disabled');

            if (this.topMessager)
                this.alert('数据处理中...');
            var sendOpts = {
                url: options.url,
                method: options.method || 'post',
                data: options.data || {},
                onSuccess: function (json) {
                    if (json.status == 1) {
                        if (json.msg)
                            self.alert(json.msg, 'success', true);
                        if (options.success)
                            options.success(json);
                    } else {
                        if (options.fail)
                            options.fail(json);
                        else
                            self.alert(json.msg, 'error', true);
                    }
                },
                onComplete: function () {
                    if (options.button)
                        options.button.removeProperty('disabled');
                },
                onFailure: function () {
                    self.alert('请求出错了...', 'error', true);
                }
            };

            return new Request.JSON(sendOpts);
        },

        alert: function (msg, type, autoClose) {
            if (this.topMessager) {
                if (msg) {
                    type = type || 'warning';
                    this.topMessager.getElement('.alert').set('html', msg).set('class', 'alert alert-' + type);
                    new Element('button', {
                        'html': '×',
                        'class': 'close'
                    }).inject(this.topMessager.getElement('.alert'), 'top');
                    this.topMessager.tween(-this.topMessager.outerHeight(), -1);
                } else if (this.topMessager.getElement('.alert').get('text')) {
                    this.topMessager.tween(-this.topMessager.outerHeight(), -1);
                } else {
                    //this.topMessager.tween(-1, -this.topMessager.outerHeight());
                    this.alertHide();
                }

                if (autoClose)
                    this.alertHide.bind(this).delay(5000);
            } else {
                try {
                    new OpenBox.Alert(msg);
                } catch (e) {
                    alert(msg);
                }
            }
        },

        alertHide: function () {
            if (this.topMessager)
                this.topMessager.tween(-1, -this.topMessager.outerHeight());
        }
    });

    Locale.use('zh-CHS');
})();
