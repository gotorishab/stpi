# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import lxml
import requests
import logging
import werkzeug.exceptions
import werkzeug.urls
import werkzeug.wrappers

from datetime import datetime

from odoo import http, tools, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.addons.website_profile.controllers.main import WebsiteProfile
from odoo.addons.portal.controllers.portal import _build_url_w_params

from odoo.http import request

_logger = logging.getLogger(__name__)


class WebsiteForum(http.Controller):

    @http.route('/forum/new/group', type='json', auth="user", methods=['POST'], website=True)
    def forum_create(self, group_name="New Group", group_user=False):
        group_data = {
            'name': group_name,
        }
        group_obj = request.env['res.groups'].sudo().create(group_data)
        users = request.env['res.users'].sudo().search([('id','=', group_user)]) 
        group_obj.users = [(4, user.id) for user in users]
        return True
