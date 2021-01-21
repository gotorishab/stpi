odoo.define('custom_forum.create_group_btn', function (require) {
'use strict';
var core = require('web.core');
var ajax = require('web.ajax');
var qweb = core.qweb;
ajax.loadXML('/custom_forum/static/src/xml/website_forum_templates.xml', qweb);
});