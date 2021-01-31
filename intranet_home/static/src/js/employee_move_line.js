odoo.define('hr_applicant_portal.hr_applicant_portal', function (require) {
'use strict';

var sAnimation = require('website.content.snippets.animation');
var core = require('web.core');
var weDefaultOptions = require('web_editor.wysiwyg.default_options');
var wysiwygLoader = require('web_editor.loader');
var publicWidget = require('web.public.widget');
var session = require('web.session');
var qweb = core.qweb;

var _t = core._t;

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
    publicWidget.registry.websitePost = publicWidget.Widget.extend({
        selector: '.website_blog',
        events: {
            'click .vote_up, .vote_down': '_onVotePostClick',
        },

        /**
         * @private
         * @param {Event} ev
         */
        _onVotePostClick: function (ev) {
            var self = this;
            ev.preventDefault();
            var $btn = $(ev.currentTarget);
            this._rpc({
                route: $btn.data('href'),
            }).then(function (data) {
                if (data.error) {
                    var message;
                    if (data.error === 'own_post') {
                        message = _t('Sorry, you cannot vote for your own posts');
                    } else if (data.error === 'anonymous_user') {
                        message = _t('Sorry you must be logged to vote');
                    }
                    self.call('crash_manager', 'show_warning', {
                        message: message,
                        title: _t("Access Denied"),
                    }, {
                        sticky: false,
                    });
                } else {
                    var $container = $btn.closest('.vote');
                    var $items = $container.children();
                    var $voteUp = $items.filter('.vote_up');
                    var $voteDown = $items.filter('.vote_down');
                    var $voteCount = $items.filter('.vote_count');
                    var userVote = parseInt(data['user_vote']);

                    $voteUp.prop('disabled', userVote === 1);
                    $voteDown.prop('disabled', userVote === -1);

                    $items.removeClass('text-success text-danger text-muted o_forum_vote_animate');
                    void $container[0].offsetWidth; // Force a refresh

                    if (userVote === 1) {
                        $voteUp.addClass('text-success');
                        $voteCount.addClass('text-success');
                        $voteDown.removeClass('karma_required');
                    }
                    if (userVote === -1) {
                        $voteDown.addClass('text-danger');
                        $voteCount.addClass('text-danger');
                        $voteUp.removeClass('karma_required');
                    }
                    if (userVote === 0) {
                        if (!$voteDown.data('can-downvote')) {
                            $voteDown.addClass('karma_required');
                        }
                        if (!$voteUp.data('can-upvote')) {
                            $voteUp.addClass('karma_required');
                        }
                    }
                    $voteCount.html(data['vote_count']).addClass('o_forum_vote_animate');
                }
            });
        },
    });
});