odoo.define('website_forum.editor', function (require) {
"use strict";

var core = require('web.core');
var WebsiteNewMenu = require('website.newMenu');
var Dialog = require('web.Dialog');

var _t = core._t;

var GroupCreateDialog = Dialog.extend({
    xmlDependencies: Dialog.prototype.xmlDependencies.concat(
        ['/custom_forum/static/src/xml/website_forum_templates.xml']
    ),
    selector: '.website_forum',
    template: 'custom_forum.create_group_template',
    /**
     * @override
     * @param {Object} parent
     * @param {Object} options
     */
    init: function (parent, options) {
        options = _.defaults(options || {}, {
            title: _t("New Group"),
            size: 'medium',
            buttons: [
                {
                    text: _t("Create"),
                    classes: 'btn-primary',
                    click: this.onCreateGroup.bind(this),
                    close: true
                },
                {
                    text: _t("Discard"),
                    close: true
                },
            ]
        });
        this._super(parent, options);
    },
    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
                var $input_unit_id = self.$('#unit_id');
                var $input_user_ids = self.$('#user_ids');
                var $input_department_id = self.$('#department_id');
                var $input_business_type = self.$('#business_type');
                $input_unit_id.select2({
                    width: '100%',
                    allowClear: true,
                    formatNoMatches: false,
                    multiple: false,
                    selection_data: false,
                    fill_data: function (query, data) {
                        var that = this;
                        var tags = {results: []};
                        _.each(data, function (obj) {
                            if (that.matcher(query.term, obj.display_name)) {
                                tags.results.push({id: obj.id, text: obj.display_name});
                            }
                        });
                        query.callback(tags);
                    },
                    query: function (query) {
                        var that = this;
                        // fetch data only once and store it
                        if (!this.selection_data) {
                            self._rpc({
                                model: 'vardhman.unit.master',
                                method: 'search_read',
                                args: [[], ['display_name']],
                            }).then(function (data) {
                                that.fill_data(query, data);
                                that.selection_data = data;
                            });
                        } else {
                            this.fill_data(query, this.selection_data);
                        }
                    }
                });
                $input_department_id.select2({
                    width: '100%',
                    allowClear: true,
                    formatNoMatches: false,
                    multiple: false,
                    selection_data: false,
                    fill_data: function (query, data) {
                        var that = this;
                        var tags = {results: []};
                        _.each(data, function (obj) {
                            if (that.matcher(query.term, obj.display_name)) {
                                tags.results.push({id: obj.id, text: obj.display_name});
                            }
                        });
                        query.callback(tags);
                    },
                    query: function (query) {
                        var that = this;
                        // fetch data only once and store it
                        if (!this.selection_data) {
                            self._rpc({
                                model: 'hr.department',
                                method: 'search_read',
                                args: [[], ['display_name']],
                            }).then(function (data) {
                                that.fill_data(query, data);
                                that.selection_data = data;
                            });
                        } else {
                            this.fill_data(query, this.selection_data);
                        }
                    }
                });
                $input_business_type.select2({
                    width: '100%',
                    allowClear: true,
                    formatNoMatches: false,
                    multiple: false,
                    selection_data: false,
                    fill_data: function (query, data) {
                        var that = this;
                        var tags = {results: []};
                        _.each(data, function (obj) {
                            if (that.matcher(query.term, obj.display_name)) {
                                tags.results.push({id: obj.id, text: obj.display_name});
                            }
                        });
                        query.callback(tags);
                    },
                    query: function (query) {
                        var that = this;
                        // fetch data only once and store it
                        if (!this.selection_data) {
                            self._rpc({
                                model: 'vardhman.businesstype.master',
                                method: 'search_read',
                                args: [[], ['display_name']],
                            }).then(function (data) {
                                that.fill_data(query, data);
                                that.selection_data = data;
                            });
                        } else {
                            this.fill_data(query, this.selection_data);
                        }
                    }
                });
                $input_user_ids.select2({
                tags: true,
                tokenSeparators: [',', ' ', '_'],
                maximumInputLength: 35,
                minimumInputLength: 1,
                maximumSelectionSize: 5,
                lastsearch: [],
                ajax: {
                    url: '/forum/get_users',
                    dataType: 'json',
                    data: function (term) {
                        return {
                            unit_id : $input_unit_id[0].value,
                            department_id : $input_department_id[0].value,
                            business_type: $input_business_type[0].value,
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
                initSelection: function (element, callback) {
                    var data = [];
                    _.each(element.data('init-value'), function (x) {
                        data.push({id: x.id, text: x.name, isNew: false});
                    });
                    element.val('');
                    callback(data);
                },
            });
        });
    },
    onCreateGroup: function () {
        var $dialog = this.$el;
        var $groupName = $dialog.find('input[name=name]');
        if (!$groupName.val()) {
            $groupName.addClass('border-danger');
            return;
        }
        var $groupUserId = $dialog.find('input[name=user_ids]');
        return this._rpc({
            route: '/forum/new/group',
            params: {
                group_name: $groupName.val(),
                group_user: $groupUserId.val(),
            },
        }).then(function (data) {
            return
        });
    },
});

var ForumCreateDialog = Dialog.extend({
    xmlDependencies: Dialog.prototype.xmlDependencies.concat(
        ['/website_forum/static/src/xml/website_forum_templates.xml']
    ),
    template: 'website_forum.add_new_forum',
    events: _.extend({}, Dialog.prototype.events, {
        'change input[name="privacy"]': '_onPrivacyChanged',
        'click .create_group_btn': '_onCreateGroup',
    }),

    /**
     * @override
     * @param {Object} parent
     * @param {Object} options
     */
    init: function (parent, options) {
        options = _.defaults(options || {}, {
            title: _t("New Forum"),
            size: 'medium',
            buttons: [
                {
                    text: _t("Create"),
                    classes: 'btn-primary',
                    click: this.onCreateClick.bind(this),
                },
                {
                    text: _t("Discard"),
                    close: true
                },
            ]
        });
        this._super(parent, options);
    },
    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            var $input = self.$('#group_id');
            $input.select2({
                width: '100%',
                allowClear: true,
                formatNoMatches: false,
                multiple: false,
                selection_data: false,
                fill_data: function (query, data) {
                    var that = this;
                    var tags = {results: []};
                    _.each(data, function (obj) {
                        if (that.matcher(query.term, obj.display_name)) {
                            tags.results.push({id: obj.id, text: obj.display_name});
                        }
                    });
                    query.callback(tags);
                },
                query: function (query) {
                    var that = this;
                    // fetch data only once and store it
                    if (!this.selection_data) {
                        self._rpc({
                            model: 'res.groups',
                            method: 'search_read',
                            args: [[], ['display_name']],
                        }).then(function (data) {
                            that.fill_data(query, data);
                            that.selection_data = data;
                        });
                    } else {
                        this.fill_data(query, this.selection_data);
                    }
                }
            });
        });
    },
    _onCreateGroup: function () {
        $("#group_id")[0].required = true
        var self = this;
        var def = new Promise(function (resolve) {
            var dialog = new GroupCreateDialog(self, {});
            dialog.open();
            dialog.on('closed', self, resolve);
        });
        return def;
    },
    onCreateClick: function () {
        var $dialog = this.$el;
        var $forumName = $dialog.find('input[name=forum_name]');
        if (!$forumName.val()) {
            $forumName.addClass('border-danger');
            return;
        }
        var $forumPrivacyGroup = $dialog.find('input[name=group_id]');
        var forumPrivacy = $dialog.find('input:radio[name=privacy]:checked').val();
        if (forumPrivacy === 'private' && !$forumPrivacyGroup.val()) {
            this.$("#group-required").removeClass('d-none');
            return;
        }
        var addMenu = ($dialog.find('input[type="checkbox"]').is(':checked'));
        var forumMode = $dialog.find('input:radio[name=mode]:checked').val();
        return this._rpc({
            route: '/forum/new',
            params: {
                forum_name: $forumName.val(),
                forum_mode: forumMode,
                forum_privacy: forumPrivacy,
                forum_privacy_group: $forumPrivacyGroup.val(),
                add_menu: addMenu || "",
            },
        }).then(function (url) {
            window.location.href = url;
            return new Promise(function () {});
        });
    },
    /**
     * @private
     */
    _onPrivacyChanged: function (ev) {
        this.$('.show_visibility_group').toggleClass('d-none', ev.target.value !== 'private');
    },
});

WebsiteNewMenu.include({
    actions: _.extend({}, WebsiteNewMenu.prototype.actions || {}, {
        new_forum: '_createNewForum',
    }),

    //--------------------------------------------------------------------------
    // Actions
    //--------------------------------------------------------------------------

    /**
     * Asks the user information about a new forum to create, then creates it
     * and redirects the user to this new forum.
     *
     * @private
     * @returns {Promise} Unresolved if there is a redirection
     */
    _createNewForum: function () {
        var self = this;
        var def = new Promise(function (resolve) {
            var dialog = new ForumCreateDialog(self, {});
            dialog.open();
            dialog.on('closed', self, resolve);
        });
        return def;
    },
});
});
