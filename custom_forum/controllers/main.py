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

    @http.route('/forum/get_users', type='http', auth="public", methods=['GET'], website=True, sitemap=False)
    def tag_read(self, query='', limit=25, **post):
        domain = [('name', '=ilike', (query or '') + "%")]
        unit_id = post.get('unit_id') or False
        business_type = post.get('business_type') or False
        department_id = post.get('department_id') or False
        if unit_id:
            domain.append(('unit_id','=', int(unit_id)))
        if business_type:
            domain.append(('business_type','=', int(business_type)))
        if department_id:
            domain.append(('department_id','=', int(department_id)))
        data = request.env['res.users'].search_read(
                domain=domain,
                fields=['id', 'name'],
                limit=int(limit),
            )
        return json.dumps(data)

    @http.route('/forum/new/group', type='json', auth="user", methods=['POST'], website=True)
    def forum_create(self, group_name="New Group", group_user=False):
        group_data = {
            'name': group_name,
        }
        group_user = group_user.split(',')
        group_obj = request.env['res.groups'].sudo().create(group_data)
        users = request.env['res.users'].sudo().search([('id','in', group_user)])
        group_obj.users = [(4, user.id) for user in users]
        return True
