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
            $('.oe_marriage').removeClass('d-none');
            $('.oe_work').addClass('d-none');
            $('.oe_marriage_ani').addClass('active');
            $('.oe_work_ani').removeClass('active');
        },
        _onClickWork: function () {
            $('.oe_marriage').addClass('d-none');
            $('.oe_work').removeClass('d-none');
            $('.oe_marriage_ani').removeClass('active');
            $('.oe_work_ani').addClass('active');

        },
        
    });
});