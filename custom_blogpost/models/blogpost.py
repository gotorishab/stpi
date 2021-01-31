import logging
import math
import re

from datetime import datetime

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools import misc, sql
from odoo.tools.translate import html_translate
from odoo.addons.http_routing.models.ir_http import slug

_logger = logging.getLogger(__name__)

class Blog(models.Model):
    _inherit = "blog.blog"

    @api.model
    def _tag_to_write_vals(self, tags=''):
        Tag = self.env['blog.tag']
        post_tags = []
        existing_keep = []
        user = self.env.user
        for tag in (tag for tag in tags.split(',') if tag):
            if tag.startswith('_'):  # it's a new tag
                # check that not already created meanwhile or maybe excluded by the limit on the search
                tag_ids = Tag.search([('name', '=', tag[1:])])
                if tag_ids:
                    existing_keep.append(int(tag_ids[0]))
                else:
                    if len(tag):
                        post_tags.append((0, 0, {'name': tag[1:], 'front_type': 'story'}))
            else:
                existing_keep.append(int(tag))

        post_tags.insert(0, [6, 0, existing_keep])
        return post_tags