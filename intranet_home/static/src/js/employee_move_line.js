odoo.define('hr_applicant_portal.hr_applicant_portal', function (require) {
'use strict';

var sAnimation = require('website.content.snippets.animation');;
var core = require('web.core');

    sAnimation.registry.anniversary = sAnimation.Class.extend({
        selector: '.oe_anniversary',
        events: {
            'click .oe_marriage_ani': '_onClickMarriage',
            'click .oe_work_ani': '_onClickWork',
        },
        /**
         * @private
         * @param {MouseEvent} ev
         */
        _onClickMarriage: function () {
            $('#oe_marriage').removeClass('d-none');
            $('#oe_work').addClass('d-none');
        },
        _onClickWork: function () {
            $('#oe_marriage').addClass('d-none');
            $('#oe_work').removeClass('d-none');
        },
        
    });
});