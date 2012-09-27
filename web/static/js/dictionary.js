/**
 * User: Lobos841@gmail.com
 * Date: 2012-9-27
 */

(function () {
    window.Dictionary = new new Class({
        initialize: function () {
        },

        exec: function (url, fn, api) {
            switch (api) {
                default:
                    this.getIciba(url, fn);
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
                    var dict = parse(xml);
                    fn(dict);
                }
            }).get();
        }
    });
})();