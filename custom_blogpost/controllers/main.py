# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict
import json
from odoo import http, fields, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.http import request
from odoo.osv import expression
from odoo.tools import html2plaintext
from odoo.tools.misc import get_lang
from odoo.tools import sql


class WebsiteBlog(http.Controller):

    @http.route('/blog/get_tags', type='http', auth="public", methods=['GET'], website=True, sitemap=False)
    def tag_read(self, query='', limit=25, **post):
        data = request.env['blog.tag'].search_read(
            domain=[('name', '=ilike', (query or '') + "%"), ('front_type', '=', 'story')],
            fields=['id', 'name'],
            limit=int(limit),
        )
        return json.dumps(data)


    @http.route(['/blog/<model("blog.blog"):blog>/blogpost'], type='http', auth="user", website=True)
    def new_blogpost(self, blog, **post):
        user = request.env.user
        values = {
            'user':user,
            'blog': blog
        }
        if 'error' in post:
            values['error'] = post['error']
        if 'post_name' in post:
            values['post_name'] = post['post_name']
        return request.render("custom_blogpost.new_blogpost", values)


    @http.route(['/blog/<model("blog.blog"):blog>/new'],type='http', auth="user", methods=['POST'], website=True)
    def blogpost_create(self, blog, **post):
        values = {}
        user = request.env.user
        post_tag_ids = blog._tag_to_write_vals(post.get('post_tags', ''))
        new_post = request.env['vardhman.create.blogpost'].create({
            'name': post.get('post_name') or '',
            'description': post.get('content', False),
            'unit_id': user.unit_id and user.unit_id.id or False,
            'tag_ids': post_tag_ids
        })
        if new_post:
            try:
                new_post.button_send_for_approval()
            except Exception as e:
                post_name = post.get('post_name') or ''
                return werkzeug.utils.redirect("/blog/%s/blogpost?error=%s&post_name=%s" % (slug(blog), e, post_name))                
        return werkzeug.utils.redirect("/blog/%s" % (slug(blog)))