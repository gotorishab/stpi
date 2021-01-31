odoo.define('website_blog.website_blog', function (require) {
'use strict';
var core = require('web.core');
var weDefaultOptions = require('web_editor.wysiwyg.default_options');
var wysiwygLoader = require('web_editor.loader');

const dom = require('web.dom');
const publicWidget = require('web.public.widget');

publicWidget.registry.websiteBlog = publicWidget.Widget.extend({
    selector: '.website_blog',
    events: {
        'click #o_wblog_next_container': '_onNextBlogClick',
        'click #o_wblog_post_content_jump': '_onContentAnchorClick',
        'click .o_twitter, .o_facebook, .o_linkedin, .o_google, .o_twitter_complete, .o_facebook_complete, .o_linkedin_complete, .o_google_complete': '_onShareArticle',
        'submit .js_wblog_submit_form:has(:not(.karma_required).o_wblog_submit_post)': '_onSubmitForm',
    },

    /**
     * @override
     */
    start: function () {
        var self = this;
        $('.js_tweet, .js_comment').share({});

        $('input.js_select2').select2({
            tags: true,
            tokenSeparators: [',', ' ', '_'],
            maximumInputLength: 35,
            minimumInputLength: 2,
            maximumSelectionSize: 5,
            lastsearch: [],
            createSearchChoice: function (term) {
                if (_.filter(self.lastsearch, function (s) {
                    return s.text.localeCompare(term) === 0;
                }).length === 0) {
                    //check Karma
                    if (parseInt($('#karma').val()) >= parseInt($('#karma_edit_retag').val())) {
                        return {
                            id: '_' + $.trim(term),
                            text: $.trim(term) + ' *',
                            isNew: true,
                        };
                    }
                }
            },
            formatResult: function (term) {
                if (term.isNew) {
                    return '<span class="badge badge-primary">New</span> ' + _.escape(term.text);
                } else {
                    return _.escape(term.text);
                }
            },
            ajax: {
                url: '/blog/get_tags',
                dataType: 'json',
                data: function (term) {
                    return {
                        query: term,
                        limit: 50,
                    };
                },
                results: function (data) {
                    var ret = [];
                    _.each(data, function (x) {
                        ret.push({
                            id: x.id,
                            text: x.name,
                            isNew: false,
                        });
                    });
                    self.lastsearch = ret;
                    return {results: ret};
                }
            },
            // Take default tags from the input value
            initSelection: function (element, callback) {
                var data = [];
                _.each(element.data('init-value'), function (x) {
                    data.push({id: x.id, text: x.name, isNew: false});
                });
                element.val('');
                callback(data);
            },
        });

        // _.each($('textarea.o_wysiwyg_loader'), function (textarea) {
        //     var $textarea = $(textarea);
        //     var editorKarma = $textarea.data('karma') || 0; // default value for backward compatibility
        //     var $form = $textarea.closest('form');
        //     var hasFullEdit = parseInt($("#karma").val()) >= editorKarma;
        //     // Warning: Do not activate any option that adds inline style.
        //     // Because the style is deleted after save.
        //     var toolbar = [
        //         ['style', ['style']],
        //         ['font', ['bold', 'italic', 'underline', 'clear']],
        //         ['para', ['ul', 'ol', 'paragraph']],
        //         ['table', ['table']],
        //     ];
        //     if (hasFullEdit) {
        //         toolbar.push(['insert', ['link', 'picture']]);
        //     }
        //     toolbar.push(['history', ['undo', 'redo']]);

        //     var options = {
        //         height: 200,
        //         minHeight: 80,
        //         toolbar: toolbar,
        //         styleWithSpan: false,
        //         styleTags: _.without(weDefaultOptions.styleTags, 'h1', 'h2', 'h3'),
        //         recordInfo: {
        //             context: self._getContext(),
        //             res_model: 'vardhman.create.blogpost',
        //             res_id: +window.location.pathname.split('-').pop(),
        //         },
        //         disableResizeImage: true,
        //     };
        //     if (!hasFullEdit) {
        //         options.plugins = {
        //             LinkPlugin: false,
        //             MediaPlugin: false,
        //         };
        //     }
        //     wysiwygLoader.load(self, $textarea[0], options).then(wysiwyg => {
        //         // float-left class messes up the post layout OPW 769721
        //         $form.find('.note-editable').find('img.float-left').removeClass('float-left');
        //         $form.on('click', 'button .a-submit', () => {
        //             wysiwyg.save();
        //         });
        //     });
        // });


        return this._super.apply(this, arguments);
    },

    _onSubmitForm: function (ev) {
        let validForm = true;

        let $form = $(ev.currentTarget);
        let $title = $form.find('input[name=post_name]');
        let $textarea = $form.find('textarea[name=content]');
        let $post_tags = $form.find('textarea[name=post_tags]');
        // It's not really in the textarea that the user write at first
        let textareaContent = $form.find('.o_wysiwyg_wrapper .note-editable.panel-body').text().trim();

        if ($title.length && $title[0].required) {
            if ($title.val()) {
                $title.removeClass('is-invalid');
            } else {
                $title.addClass('is-invalid');
                validForm = false;
            }
        }

        // Because the textarea is hidden, we add the red or green border to its container
        if ($textarea[0] && $textarea[0].required) {
            let $textareaContainer = $form.find('.o_wysiwyg_wrapper .note-editor.panel.panel-default');
            if (!textareaContent.length) {
                $textareaContainer.addClass('border border-danger rounded-top');
                validForm = false;
            } else {
                $textareaContainer.removeClass('border border-danger rounded-top');
            }
        }
        if (!validForm) {
            ev.preventDefault();
            setTimeout(function() {
                var $buttons = $(ev.currentTarget).find('button[type="submit"], a.a-submit');
                _.each($buttons, function (btn) {
                    let $btn = $(btn);
                    $btn.find('i').remove();
                    $btn.prop('disabled', false);
                });
            }, 0);
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
    _onNextBlogClick: function (ev) {
        ev.preventDefault();
        var self = this;
        var $el = $(ev.currentTarget);
        var nexInfo = $el.find('#o_wblog_next_post_info').data();
        $el.find('.o_record_cover_container').addClass(nexInfo.size + ' ' + nexInfo.text).end()
           .find('.o_wblog_toggle').toggleClass('d-none');
        // Appending a placeholder so that the cover can scroll to the top of the
        // screen, regardless of its height.
        const placeholder = document.createElement('div');
        placeholder.style.minHeight = '100vh';
        this.$('#o_wblog_next_container').append(placeholder);

        // Use _.defer to calculate the 'offset()'' only after that size classes
        // have been applyed and that $el has been resized.
        _.defer(function () {
            self._forumScrollAction($el, 300, function () {
                window.location.href = nexInfo.url;
            });
        });
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onContentAnchorClick: function (ev) {
        ev.preventDefault();
        ev.stopImmediatePropagation();
        var $el = $(ev.currentTarget.hash);

        this._forumScrollAction($el, 500, function () {
            window.location.hash = 'blog_content';
        });
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onShareArticle: function (ev) {
        ev.preventDefault();
        var url = '';
        var $element = $(ev.currentTarget);
        var blogPostTitle = encodeURIComponent($('#o_wblog_post_name').html() || '');
        var articleURL = encodeURIComponent(window.location.href);
        if ($element.hasClass('o_twitter')) {
            var twitterText = core._t("Amazing blog article: %s! Check it live: %s");
            var tweetText = _.string.sprintf(twitterText, blogPostTitle, articleURL);
            url = 'https://twitter.com/intent/tweet?tw_p=tweetbutton&text=' + tweetText;
        } else if ($element.hasClass('o_facebook')) {
            url = 'https://www.facebook.com/sharer/sharer.php?u=' + articleURL;
        } else if ($element.hasClass('o_linkedin')) {
            url = 'https://www.linkedin.com/sharing/share-offsite/?url=' + articleURL;
        }
        window.open(url, '', 'menubar=no, width=500, height=400');
    },

    //--------------------------------------------------------------------------
    // Utils
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {JQuery} $el - the element we are scrolling to
     * @param {Integer} duration - scroll animation duration
     * @param {Function} callback - to be executed after the scroll is performed
     */
    _forumScrollAction: function ($el, duration, callback) {
        dom.scrollTo($el[0], {duration: duration}).then(() => callback());
    },
});
});
